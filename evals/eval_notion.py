from arcade.sdk.eval import (
    EvalSuite,
    EvalRubric,
    BinaryCritic,
    SimilarityCritic,
    tool_eval,
)
from arcade.sdk import ToolCatalog
from arcade_notion.tools import (
    create_page_by_parent_title,
    create_subpage,
    get_page_id,
)

catalog = ToolCatalog()
catalog.add_tool(create_page_by_parent_title, "Notion")
catalog.add_tool(create_subpage, "Notion")
catalog.add_tool(get_page_id, "Notion")

rubric = EvalRubric(
    fail_threshold=0.85,
    warn_threshold=0.95,
    fail_on_tool_selection=True,
    tool_selection_weight=1.0,
)


@tool_eval()
def notion_eval_suite() -> EvalSuite:
    suite = EvalSuite(
        name="Notion Evaluation Suite",
        system_message="You are a helpful assistant.",
        catalog=catalog,
        rubric=rubric,
    )

    # Creating page by parent title
    suite.add_case(
        name="Create page using parent title",
        user_message="Create a new page titled 'Meeting Notes' under my Team Updates page with the content '## Key Points\n- Discussion about Q4 goals\n- New project timeline'",
        expected_tool_calls=[
            (
                create_page_by_parent_title,
                {
                    "parent_title": "Team Updates",
                    "title": "Meeting Notes",
                    "content": "## Key Points\n- Discussion about Q4 goals\n- New project timeline",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="parent_title", weight=0.4),
            BinaryCritic(critic_field="title", weight=0.3),
            SimilarityCritic(
                critic_field="content", weight=0.3, similarity_threshold=0.95
            ),
        ],
    )

    # Getting page ID
    suite.add_case(
        name="Get page ID",
        user_message="What's the ID of the page titled Project Roadmap?",
        expected_tool_calls=[
            (
                get_page_id,
                {
                    "title": "Project Roadmap",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="title", weight=1.0),
        ],
    )

    # Create subpage with ID
    suite.add_case(
        name="Create subpage with parent ID",
        user_message="Create a new page under the page with ID 135063722f5d80509f45f6c9290d456 titled Weekly Report with All tasks are on track",
        expected_tool_calls=[
            (
                create_subpage,
                {
                    "parent_id": "135063722f5d80509f45f6c9290d456",
                    "title": "Weekly Report",
                    "content": "All tasks are on track",
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="parent_id", weight=0.4),
            BinaryCritic(critic_field="title", weight=0.3),
            SimilarityCritic(
                critic_field="content", weight=0.3, similarity_threshold=0.95
            ),
        ],
    )

    # Demo Recipe to use in the evaluation
    chicken_parmesan_recipe = """
      Here's a simple recipe for Chicken Parmesan:
        Ingredients:

        • 2 boneless, skinless chicken breasts
        • Salt and pepper to taste 
        • 1 cup all-purpose flour
        • 2 large eggs
        • 1 cup breadcrumbs (preferably Italian-style)
        • 1/2 cup grated Parmesan cheese
        • 1 cup marinara sauce
        • 1 cup shredded mozzarella cheese
        • 1/4 cup fresh basil leaves, chopped (optional)
        • Olive oil for frying

        Instructions:

        1 Prepare the Chicken:
          • Preheat your oven to 400°F (200°C).
          • Slice the chicken breasts in half horizontally to create 4 thinner cutlets.
          • Season both sides with salt and pepper.
        2 Coating Process:
          • Place flour in a shallow dish.
          • Beat eggs in another shallow dish.
          • Mix breadcrumbs and grated Parmesan in a third shallow dish.
        3 Bread the Chicken:
          • Dredge each chicken piece in flour, shaking off excess.
          • Dip into beaten eggs, ensuring it's completely coated.
          • Finally, press into the breadcrumb mixture, coating evenly.
        4 Cook the Chicken:
          • In a large skillet, heat olive oil over medium heat.
          • Add chicken and cook until golden brown on both sides, about 3-4 minutes per side. Transfer to a paper towel-lined
            plate to drain.
        5 Assemble and Bake:
          • Spread a thin layer of marinara sauce on the bottom of a baking dish.
          • Place chicken cutlets in the dish.
          • Spoon more marinara sauce over the chicken.
          • Sprinkle shredded mozzarella evenly over the top.
        6 Bake:
          • Bake in the preheated oven for 15-20 minutes, or until the cheese is melted and bubbly.
        7 Garnish and Serve:
          • Sprinkle with fresh basil if desired.
          • Serve with pasta or a side salad.

        Enjoy your homemade Chicken Parmesan!
    """

    # Create a page with previous content
    suite.add_case(
        name="Create a page with previous content",
        user_message="Create a page for this Chicken Parmesan recipe in my Recipes page in Notion",
        additional_messages=[
            {"role": "user", "content": "Create a recipe for a chicken parmesan"},
            {
                "role": "assistant",
                "content": chicken_parmesan_recipe,
            },
        ],
        expected_tool_calls=[
            (
                create_page_by_parent_title,
                {
                    "parent_title": "Recipes",
                    "title": "Chicken Parmesan",
                    "content": chicken_parmesan_recipe,
                },
            )
        ],
        critics=[
            BinaryCritic(critic_field="parent_title", weight=0.4),
            SimilarityCritic(
                critic_field="title",
                weight=0.3,
                similarity_threshold=0.7,
            ),
            SimilarityCritic(
                critic_field="content", weight=0.3, similarity_threshold=0.9
            ),
        ],
    )

    # Test ambiguous request
    suite.add_case(
        name="Ambiguous request",
        additional_messages=[
            {"role": "user", "content": "Create a recipe for a chicken parmesan"},
            {
                "role": "assistant",
                "content": chicken_parmesan_recipe,
            },
        ],
        user_message="add the recipe to my recipes page in Notion",
        expected_tool_calls=[
            (
                create_page_by_parent_title,
                {
                    "parent_title": "Recipes",
                    "title": "Chicken Parmesan",
                    "content": chicken_parmesan_recipe,
                },
            )
        ],
        critics=[
            SimilarityCritic(
                critic_field="parent_title", weight=0.4, similarity_threshold=0.8
            ),
            SimilarityCritic(
                critic_field="title",
                weight=0.3,
                similarity_threshold=0.8,
            ),
            SimilarityCritic(
                critic_field="content", weight=0.3, similarity_threshold=0.8
            ),
        ],
    )

    return suite

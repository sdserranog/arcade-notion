# Notion Toolkit


|             |                |
|-------------|----------------|
| Name        | notion |
| Package     | arcade_notion |
| Repository  | None   |
| Version     | 0.1.1      |
| Description | Notion integration to search, create, update, and delete databases/pages.  |
| Author      | sdserranog@gmail.com      |


| Tool Name   | Description                                                             |
|-------------|-------------------------------------------------------------------------|
| CreateSubpage | Create a new page under a parent page using its ID. |
| CreatePageByParentTitle | Creates a new page under an existing Notion page or database. |
| GetPageId | Finds and returns the ID of a Notion page by searching for its title. Only use when page ID is explicitly required. |


### CreateSubpage
Create a new page under a parent page using its ID.

#### Parameters
- `parent_id`*(string, required)* ID of the parent page
- `title`*(string, required)* Title for the new page
- `content`*(string, required)* Content in markdown format.

---

### CreatePageByParentTitle
Creates a new page under an existing Notion page or database.

#### Parameters
- `parent_title`*(string, required)* Title of an existing page/database where the new page will be created, no need to include the page ID
- `title`*(string, required)* Title for your new page
- `content`*(string, required)* Content in markdown format.

---

### GetPageId
Finds and returns the ID of a Notion page by searching for its title. Only use when page ID is explicitly required.

#### Parameters
- `title`*(string, required)* Title of the page to find

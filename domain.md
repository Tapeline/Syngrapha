# Domain

## Glossary

Syngrapha domain defines following terms:

<a id="product"></a>

**Product** - a single bought item. It has:
- product - text - describes type of the item in free form
- count - integer - how many items of that type were bought
- category - [Category](#category) - in which category does this item belong to
- price - integer - how much does one item cost
- (calculated) cost - how much does the whole product cost

<a id="transaction"></a>

**Transaction** - a collection of [Products](#product) which were bought at
one time in one place. Has at least one [Product](#product). Has fields:
- products - list of [Products](#product)
- time - date&time - when were the products bought
- merchant - text - where were the products bought (in free form)
- (calculated) cost - how much was spent

<a id="category"></a>

**Category** - a category of [Product](#product). Member of a finite predefined collection:
- Bread products
- Milk products
- Fruits and berries
- Grains
- Meat products
- Confectionery
- Vegetables
- Drinks
- Other products
- (to be extended to include not only food)

<a id="metacategory"></a>

**Metacategory** - a super-category of [Product](#product). Includes one or more 
[Categories](#category) in itself. One [Category](#category) can only be in one 
[Metacategory](#metacategory). Can be:
- Food
- Health & Care
- Transportation
- Clothing
- Home
- Restaurants
- Telecommunications
- Utility bills
- Studying
- Other

<a id="autocat-proc"></a>

**Auto-categorization process** - a long-running process of automatic categorization of
product using AI service running by. Carries info about what [Products](#product)
it affects.

## Business scenarios

### QR bill import

1. User scans QR code
2. Request to irkkt-mobile.nalog.ru for authorization
3. User is prompted to enter the confirmation code
4. Request to irkkt-mobile.nalog.ru for bill info retrieval
5. A [Transaction](#transaction) with [Products](#product) is created
6. A notification to AI categorizer is sent - the 
    [auto-categorization process](#autocat-proc) is started
7. (some time after) the categories are marked by AI categorizer

### Product table import

1. User uploads table file
2. Table file is parsed
3. For each row in uploaded table create a new [Transaction](#transaction) which
    consists of one [Product](#product) defined by properties in that row
4. Deduplicate loaded [Transactions](#transaction) with existing [Transactions](#transaction)
    using cost and date
5. Save deduplicated [Transactions](#transaction)
6. A notification to AI categorizer is sent - the 
    [auto-categorization process](#autocat-proc) is started

### Manual creation

1. User inputs [Transaction](#transaction) data and associated [Products](#product)
2. Save inputted entities

### Cancel auto-categorization process

1. User presses cancel button
2. [Process](#autocat-proc) is cancelled

### Get running auto-categorizations

1. User requests list of [Processes](#autocat-proc)
2. List of [Processes](#autocat-proc) is returned

### Get products grouped by metacategory

1. User requests list of [Products](#product) and provides time filter
2. List of grouped [Products](#product) is returned

### Get products grouped by category

1. User requests list of [Products](#product) and provides time filter
2. List of grouped [Products](#product) is returned

### Get list of transactions

1. User requests list of [Transactions](#transaction) and provides time filter
2. List of [Transactions](#transaction) is returned

### Export to table

1. User requests export
2. Data is retrieved
3. .xlsx file is exported, containing two sheets: [Transactions](#transaction) 
    and [Products](#product)

### Delete transaction

1. User requests deletion
2. [Transaction](#transaction) is deleted

### Update category on product

1. User requests update
2. If any [auto-categorization process](#autocat-proc) is undergoing on this 
    [Product](#product) -- cancel
3. Update [Category](#category)

## Events

### Auto-categorizaton process start
Issued on [Table upload](#product-table-import) and [QR import](#qr-bill-import)

### Auto-categorization process cancel
Issued on [cancel of such process](#cancel-auto-categorization-process)

### Auto-categorization process finish
Issued on finish of [auto-categorization process](#autocat-proc). 

Upon its receiving the categories are marked accordingly.

# Database Management System (BCS-501)

*AKTU B.Tech CSE, 3rd Year, Odd Semester - Revision Notebook*
*Compiled for: Harsh Katiyar, PSIT Kanpur*

---

## Unit 1: Architecture & ER Modeling

### Q1. Explain the three-schema architecture (Internal, Conceptual, External) and how it achieves physical and logical data independence. (7 Marks)

**1. Introduction / Definition**

The **three-schema architecture** (ANSI/SPARC architecture) separates a database into three levels of abstraction: the **external**, **conceptual** and **internal** level. Its main goal is to separate the user's view of the data from the way it is physically stored. This separation gives us **data independence**.

**2. Block Diagram**

```
   +-----------+     +-----------+     +-----------+
   |  User 1   |     |  User 2   |     |  User n   |
   +-----+-----+     +-----+-----+     +-----+-----+
         |                 |                 |
   +-----v-----+     +-----v-----+     +-----v-----+
   | External  |     | External  |     | External  |    EXTERNAL LEVEL
   |  View 1   |     |  View 2   |     |  View n   |    (User views)
   +-----+-----+     +-----+-----+     +-----+-----+
         |                 |                 |
         +-----------------+-----------------+
                           |
            External / Conceptual Mapping   <-- Logical Data Independence
                           |
               +-----------v-----------+
               |   Conceptual Schema   |              CONCEPTUAL LEVEL
               | (Entities, Relations, |              (Community view)
               |  Constraints, Types)  |
               +-----------+-----------+
                           |
            Conceptual / Internal Mapping   <-- Physical Data Independence
                           |
               +-----------v-----------+
               |    Internal Schema    |              INTERNAL LEVEL
               | (Files, Indexes, Data |              (Physical storage)
               |  structures, Paths)   |
               +-----------+-----------+
                           |
                   +-------v-------+
                   | Stored Database|
                   |    (Disk)      |
                   +---------------+
```

**3. Core Explanation / Working**

*(a) Internal Level (Physical Level)*

- Lowest level of abstraction. Describes **how** data is actually stored on disk.
- Covers storage structures, file organization, indexes, hashing, compression, record placement and access paths.
- Example: `STUDENT` records stored in a B+ tree file indexed on `Roll_No`.

*(b) Conceptual Level (Logical Level)*

- Describes **what** data is stored in the whole database and the relationships among the data.
- Hides physical storage details. Covers entities, attributes, data types, relationships, constraints and security.
- Designed and managed by the **DBA**.
- Example: `STUDENT(Roll_No, Name, DOB, Dept_ID)`, `DEPARTMENT(Dept_ID, DName)`.

*(c) External Level (View Level)*

- Highest level. Describes only the **part** of the database that a particular user group needs.
- Many external views can exist for one conceptual schema.
- Example: the Accounts section sees `(Roll_No, Name, Fee_Status)`. The Exam cell sees `(Roll_No, Name, Marks)`.

*(d) Mappings*

- **External/Conceptual mapping:** translates a request on a user view into a request on the conceptual schema.
- **Conceptual/Internal mapping:** translates conceptual records into stored records and access paths.

*(e) Data Independence*

- **Physical data independence:** the internal schema can change without changing the conceptual schema or application programs. Only the conceptual/internal mapping is updated.
  - Example: adding an index, moving to a new disk, or changing a file from heap to hashed organization.
- **Logical data independence:** the conceptual schema can change without changing external views or application programs. Only the external/conceptual mapping is updated.
  - Example: adding a new attribute `Email` to `STUDENT`, or splitting one table into two.
  - It is harder to achieve than physical independence, because applications depend directly on the logical structure.

**4. Key Characteristics - Physical vs. Logical Data Independence**

| Basis | Physical Data Independence | Logical Data Independence |
|---|---|---|
| Change made at | Internal level | Conceptual level |
| Protected level | Conceptual schema | External schemas / views |
| Mapping updated | Conceptual / Internal | External / Conceptual |
| Example change | New index, new storage device | Add/remove attribute or table |
| Ease of achieving | Easy | Difficult |
| Concerned with | Storage efficiency | Structure of data |

**5. Advantages & Disadvantages**

*Advantages*

- Gives data independence, which lowers application maintenance cost.
- Each user gets a customised view, which improves **security** by hiding unrelated data.
- The DBA can tune physical storage without affecting users.
- Supports many users with different needs on one shared database.

*Disadvantages*

- Mapping between levels adds **processing overhead** and can slow queries.
- More complex to design and to implement in the DBMS.
- Full logical independence is hard to achieve in practice.

**6. Conclusion / Application**

The three-schema architecture is the basis of all modern RDBMSs, such as Oracle, MySQL and PostgreSQL, where SQL **views** are the external level and **tablespaces/indexes** are the internal level.

---

### Q2. Differentiate between Generalization, Specialization and Aggregation using concrete examples. (7 Marks)

**1. Introduction / Definition**

Generalization, specialization and aggregation are **Enhanced ER (EER)** concepts that model **class hierarchies** and **relationships among relationships**. Generalization and specialization use the **IS-A** relationship (inheritance). Aggregation treats a relationship set as a higher-level entity.

**2. Diagrams**

*(a) Generalization (Bottom-Up)*

```
     +--------+          +--------+
     |  CAR   |          | TRUCK  |       Lower-level entities
     +---+----+          +----+---+       (common attributes found)
         |                    |
         +---------+----------+
                   |
                  / \
                 /ISA\                    Triangle = IS-A
                /_____\
                   |
              +----v----+
              | VEHICLE |                 Higher-level entity (created)
              +---------+
     Common attrs moved up: Reg_No, Model, Price
```

*(b) Specialization (Top-Down)*

```
              +----------+
              | EMPLOYEE |                Higher-level entity
              +----+-----+  (Emp_ID, Name, Salary)
                   |
                  / \
                 /ISA\
                /_____\
                   |
         +---------+----------+
         |                    |
   +-----v-----+       +------v-----+
   | ENGINEER  |       |  MANAGER   |     Sub-classes created
   +-----------+       +------------+
   (Skill)             (Allowance)        Specific attributes added
```

*(c) Aggregation*

```
     +-----------------------------------------------+
     |                 (Aggregated Entity)           |
     |  +----------+     /---------\    +---------+  |
     |  | EMPLOYEE |----< WORKS_ON  >---| PROJECT |  |
     |  +----------+     \---------/    +---------+  |
     +-----------------------+-----------------------+
                             |
                        /---------\
                       < MONITORS  >
                        \---------/
                             |
                       +-----+-----+
                       |  MANAGER  |
                       +-----------+
   MANAGER monitors the whole (EMPLOYEE works on PROJECT) relationship.
```

**3. Core Explanation / Working**

*(a) Generalization*

- A **bottom-up** process: two or more lower-level entities with common attributes are combined into a **single higher-level entity**.
- Common attributes move to the super-class. Distinct attributes stay in the sub-classes.
- Example: `CAR (Reg_No, Model, Seats)` and `TRUCK (Reg_No, Model, Load_Capacity)` are generalized into `VEHICLE (Reg_No, Model)`.

*(b) Specialization*

- A **top-down** process: a higher-level entity is divided into **sub-classes** based on a distinguishing feature.
- Sub-classes **inherit** all attributes and relationships of the super-class and add their own.
- Example: `EMPLOYEE` is specialized into `ENGINEER (Skill)` and `MANAGER (Allowance)`.

*(c) Constraints on Generalization/Specialization*

- **Disjoint:** an entity belongs to at most one sub-class (an employee is either an Engineer or a Manager).
- **Overlapping:** an entity may belong to more than one sub-class (a person can be both a Student and an Employee).
- **Total participation:** every super-class entity must belong to some sub-class.
- **Partial participation:** some super-class entities may belong to no sub-class.

*(d) Aggregation*

- The ER model **cannot express relationships between relationships**.
- Aggregation is an **abstraction** in which a relationship set, together with its participating entity sets, is treated as **one higher-level entity**.
- Example: `EMPLOYEE --WORKS_ON-- PROJECT` is aggregated, and `MANAGER` then has a `MONITORS` relationship with this aggregate.
- Without aggregation we would need a ternary relationship, which causes **redundancy**.

**4. Key Characteristics - Comparison Table**

| Basis | Generalization | Specialization | Aggregation |
|---|---|---|---|
| Approach | Bottom-up | Top-down | Abstraction of a relationship |
| Process | Combines entities into a super-class | Splits an entity into sub-classes | Treats a relationship as an entity |
| Relationship type | IS-A | IS-A | HAS-A / Part-of |
| Size of schema | Reduces | Increases | Avoids redundant ternary relationships |
| Inheritance | Sub-class attributes move up | Sub-classes inherit from super-class | No inheritance |
| Example | Car, Truck -> Vehicle | Employee -> Engineer, Manager | (Employee-Works_On-Project) monitored by Manager |

**5. Advantages & Disadvantages**

*Advantages*

- Generalization removes **redundancy** of common attributes.
- Specialization models real-world **sub-types** precisely, with their own attributes.
- Aggregation can model **relationships among relationships** without redundant ternary sets.
- Together they make the ER diagram closer to object-oriented design.

*Disadvantages*

- They make the ER diagram more **complex** to read and draw.
- Mapping these hierarchies to tables needs extra design choices (one table per class, or one table for the whole hierarchy), which can cause **NULL values** or extra joins.

**6. Conclusion / Application**

These EER concepts are used to design databases for **ERP, banking and university systems**, where entity hierarchies (Employee types, Account types) and monitored relationships (Project supervision) are common.

---

### Q3. List and explain E.F. Codd's 12 rules that define a fully relational database system. (7 Marks)

**1. Introduction / Definition**

In 1985 **Dr. E.F. Codd**, the father of the relational model, proposed **13 rules (Rule 0 to Rule 12)**. A DBMS must satisfy them to be called a **fully relational DBMS**. They make sure the system manages data **only through its relational capabilities**.

**2. Block Diagram - Classification of Codd's Rules**

```
                      +----------------------------+
                      |  Rule 0: Foundation Rule   |
                      +-------------+--------------+
                                    |
     +------------------+-----------+-----------+--------------------+
     |                  |                       |                    |
+----v------+   +-------v-------+     +---------v--------+   +-------v-------+
| STRUCTURE |   | DATA HANDLING |     |  INDEPENDENCE    |   |   INTEGRITY   |
|  RULES    |   |    RULES      |     |     RULES        |   |  & SECURITY   |
+-----------+   +---------------+     +------------------+   +---------------+
| R1 Info   |   | R5 Sublanguage|     | R8 Physical DI   |   | R10 Integrity |
| R2 Access |   | R6 View update|     | R9 Logical DI    |   |     indep.    |
| R3 NULLs  |   | R7 Set-level  |     | R11 Distribution |   | R12 Non-      |
| R4 Catalog|   |    ops        |     |     indep.       |   |   subversion  |
+-----------+   +---------------+     +------------------+   +---------------+
```

**3. Core Explanation - The Rules**

- **Rule 0 - Foundation Rule:** the system must manage databases **entirely** through its relational capabilities.
- **Rule 1 - Information Rule:** all information, including metadata, is represented **only as values in tables** (rows and columns).
- **Rule 2 - Guaranteed Access Rule:** every value must be reachable by the combination **Table name + Primary key value + Column name**, without using pointers.
- **Rule 3 - Systematic Treatment of NULL Values:** NULL must be handled consistently as **missing or inapplicable** information, distinct from zero or a blank string.
- **Rule 4 - Active Online Catalog (Data Dictionary):** the database description (metadata) is stored **in tables** and can be queried with the same language used for data.
- **Rule 5 - Comprehensive Data Sub-language Rule:** at least one language (like **SQL**) must support data definition, data manipulation, views, integrity constraints, authorization and transaction control.
- **Rule 6 - View Updating Rule:** every view that is **theoretically updatable** must be updatable by the system.
- **Rule 7 - High-Level Insert, Update, Delete:** insert, update and delete must work on **sets of rows** at a time, not only on a single row.
- **Rule 8 - Physical Data Independence:** changes to storage or access methods must **not affect** application programs.
- **Rule 9 - Logical Data Independence:** changes to the logical structure (such as adding a column or splitting a table) must **not affect** applications or views.
- **Rule 10 - Integrity Independence:** integrity constraints are defined in the sub-language and **stored in the catalog**, not in application programs.
- **Rule 11 - Distribution Independence:** users must not be aware whether data is **distributed** across sites. Applications keep working when data is distributed.
- **Rule 12 - Non-Subversion Rule:** if a low-level (record-at-a-time) interface exists, it must **not bypass** the integrity and security rules of the relational language.

**4. Key Characteristics - Rule Summary Table**

| Rule | Name | Key Idea |
|---|---|---|
| 0 | Foundation | Fully relational management |
| 1 | Information | Everything stored in tables |
| 2 | Guaranteed Access | Table + PK + Column |
| 3 | NULL Treatment | Uniform handling of missing values |
| 4 | Online Catalog | Metadata stored as tables |
| 5 | Data Sub-language | One complete language (SQL) |
| 6 | View Updating | Updatable views are updatable |
| 7 | Set-level Operations | Insert/Update/Delete on sets |
| 8 | Physical DI | Storage changes are invisible |
| 9 | Logical DI | Schema changes are invisible |
| 10 | Integrity Independence | Constraints stored in catalog |
| 11 | Distribution Independence | Location transparency |
| 12 | Non-subversion | No bypassing of constraints |

*Note:* no commercial RDBMS (Oracle, MySQL, SQL Server) satisfies **all 12 rules fully**. Most satisfy about 8-10 rules. Rules 6, 9 and 11 are the ones most often only partly met.

**5. Advantages & Disadvantages**

*Advantages (of following Codd's rules)*

- They give a **standard benchmark** for judging whether a DBMS is truly relational.
- They ensure **data independence, integrity and security**.
- They promote set-based processing, which makes queries **simpler and more powerful**.

*Disadvantages*

- Strict compliance is **hard to implement**, and no commercial product achieves it fully.
- Some rules, like full view updatability, are **theoretically complex** and can reduce performance.

**6. Conclusion / Application**

Codd's rules are the **yardstick used by vendors and academics** to rate RDBMS products such as Oracle, DB2 and PostgreSQL on how relational they are.

---

### Q4. Short Definitions (2 Marks Each)

**(a) Data Dictionary**

- A **data dictionary** is a centralized repository of **metadata** ("data about data").
- It stores table names, attribute names, data types, constraints, indexes, views, users and access rights.
- An **active** data dictionary is updated automatically by the DBMS. A **passive** one is maintained manually.
- Example: `INFORMATION_SCHEMA` in MySQL.

**(b) Database Schema vs. Instance**

| Schema | Instance |
|---|---|
| The **logical design / structure** of the database | The **actual data** stored at a particular moment |
| Defined once using DDL, rarely changes | Changes frequently with every insert/update/delete |
| Like a variable's type declaration | Like a variable's value |
| Example: `STUDENT(Roll, Name, Age)` | Example: `(101, 'Harsh', 21)` |

**(c) Responsibilities of a DBA (Database Administrator)**

- **Schema definition:** creates the conceptual schema using DDL.
- **Storage structure and access method definition:** chooses file organization and indexes.
- **Granting authorization:** controls user access and privileges (GRANT/REVOKE).
- **Backup and recovery:** takes periodic backups and restores after failures.
- **Integrity constraint specification:** defines rules to keep data consistent.
- **Performance tuning and monitoring:** monitors performance and tunes queries.

---

## Unit 2: Relational Algebra & Calculus

### Q1. Explain fundamental and derived relational algebra operators, with focus on Natural Join, Outer Joins and the Division operator. (7 Marks)

**1. Introduction / Definition**

**Relational algebra** is a **procedural** query language. It takes one or more relations as input and produces a new relation as output. Its operators are divided into **fundamental** (basic) operators and **derived** operators, which can be expressed using the basic ones.

**2. Block Diagram - Classification of Operators**

```
                        +----------------------+
                        |  Relational Algebra  |
                        |      Operators       |
                        +----------+-----------+
                                   |
             +---------------------+----------------------+
             |                                            |
   +---------v----------+                     +-----------v-----------+
   |    FUNDAMENTAL     |                     |        DERIVED        |
   +--------------------+                     +-----------------------+
   | Select      (σ)    |                     | Intersection   (∩)    |
   | Project     (π)    |                     | Natural Join   (⋈)    |
   | Union       (∪)    |                     | Theta Join     (⋈θ)   |
   | Set Diff.   (−)    |                     | Outer Joins (⟕ ⟖ ⟗)   |
   | Cartesian   (×)    |                     | Division       (÷)    |
   | Rename      (ρ)    |                     | Assignment     (←)    |
   +--------------------+                     +-----------------------+
```

**3. Core Explanation / Working**

*(a) Fundamental Operators*

- **Select (σ):** chooses **rows** that satisfy a predicate. `σ Dept='CSE' (STUDENT)`
- **Project (π):** chooses **columns** and removes duplicates. `π Name, Dept (STUDENT)`
- **Union (∪):** all tuples in R or S. R and S must be **union compatible** (same degree and domains).
- **Set Difference (−):** tuples in R but not in S.
- **Cartesian Product (×):** every tuple of R combined with every tuple of S. Result size is |R| x |S|.
- **Rename (ρ):** renames a relation or its attributes. `ρ S(STUDENT)`

*(b) Derived Operators*

- **Intersection:** `R ∩ S = R − (R − S)`
- **Theta Join:** `R ⋈θ S = σθ (R × S)`

**Sample relations used below**

```
 EMP                          DEPT
 +-----+-------+-----+        +-----+-------+
 | EID | Name  | DID |        | DID | DName |
 +-----+-------+-----+        +-----+-------+
 |  1  | Amit  | 10  |        | 10  | CSE   |
 |  2  | Riya  | 20  |        | 20  | IT    |
 |  3  | Karan | 40  |        | 30  | ECE   |
 +-----+-------+-----+        +-----+-------+
```

*(c) Natural Join (EMP ⋈ DEPT)*

- Joins on **all common attributes** (here `DID`) with an equality condition and keeps **one copy** of each common column.
- Formula: `R ⋈ S = π (R ∪ S attrs) ( σ R.A = S.A (R × S) )`

```
 +-----+-------+-----+-------+
 | EID | Name  | DID | DName |
 +-----+-------+-----+-------+
 |  1  | Amit  | 10  | CSE   |
 |  2  | Riya  | 20  | IT    |
 +-----+-------+-----+-------+
```

*(d) Outer Joins*

- They keep **unmatched tuples** as well, filling the missing values with **NULL**. This avoids the information loss of a natural join.
- **Left Outer Join (EMP ⟕ DEPT):** all EMP tuples are kept.
- **Right Outer Join (EMP ⟖ DEPT):** all DEPT tuples are kept.
- **Full Outer Join (EMP ⟗ DEPT):** all tuples of both relations are kept.

```
 LEFT OUTER JOIN                 RIGHT OUTER JOIN
 +---+-------+----+-------+      +------+------+----+-------+
 |EID| Name  |DID | DName |      | EID  | Name |DID | DName |
 +---+-------+----+-------+      +------+------+----+-------+
 | 1 | Amit  | 10 | CSE   |      |  1   | Amit | 10 | CSE   |
 | 2 | Riya  | 20 | IT    |      |  2   | Riya | 20 | IT    |
 | 3 | Karan | 40 | NULL  |      | NULL | NULL | 30 | ECE   |
 +---+-------+----+-------+      +------+------+----+-------+

 FULL OUTER JOIN = rows of both tables above (Amit, Riya, Karan + ECE)
```

*(e) Division Operator (R ÷ S)*

- Used for **"for all"** queries, for example "find students who are enrolled in **all** courses".
- If R(A, B) and S(B), then R ÷ S gives every A value that is paired with **every** B value in S.
- Formula: `R ÷ S = π A (R) − π A ( (π A (R) × S) − R )`

```
 ENROLLED (R)          COURSE (S)        R ÷ S
 +---------+--------+   +--------+        +---------+
 | Student | Course |   | Course |        | Student |
 +---------+--------+   +--------+        +---------+
 |    A    |   C1   |   |   C1   |        |    A    |
 |    A    |   C2   |   |   C2   |        |    C    |
 |    B    |   C1   |   +--------+        +---------+
 |    C    |   C1   |
 |    C    |   C2   |
 |    C    |   C3   |
 +---------+--------+
```

- *Step-by-step:*
  1. `π Student (R)` = {A, B, C}
  2. `π Student (R) × S` = {AC1, AC2, BC1, BC2, CC1, CC2}
  3. Subtract R: {BC2}. These are the missing pairs.
  4. `π Student` of step 3 = {B}
  5. {A, B, C} − {B} = **{A, C}**

**4. Key Characteristics - Join Comparison**

| Join Type | Condition | Unmatched Tuples | Duplicate Columns |
|---|---|---|---|
| Theta Join | Any condition (<, >, =, etc.) | Discarded | Kept |
| Equi Join | Only equality (=) | Discarded | Kept |
| Natural Join | Equality on common attributes | Discarded | Removed |
| Left Outer | Equality | Left side kept (NULL padding) | Removed |
| Right Outer | Equality | Right side kept (NULL padding) | Removed |
| Full Outer | Equality | Both sides kept | Removed |

**5. Advantages & Disadvantages**

*Advantages*

- It is the **formal foundation** of SQL and of query optimization.
- Operators are **closed**: the output is always a relation, so operations can be **nested**.
- Derived operators like join and division make complex queries **shorter**.

*Disadvantages*

- It is **procedural**: the user must specify *how* to get the result.
- It lacks aggregation, sorting and recursion in its basic form.
- Cartesian products and joins on large tables can be very **costly**.

**6. Conclusion / Application**

Relational algebra is used **internally by the query optimizer** of every RDBMS to turn SQL into efficient execution plans, for example by pushing selections before joins.

---

### Q2. Differentiate between Tuple Relational Calculus (TRC) and Domain Relational Calculus (DRC) with syntax. (7 Marks)

**1. Introduction / Definition**

**Relational calculus** is a **non-procedural (declarative)** query language based on first-order predicate logic. The user states *what* data is required, not *how* to get it. It has two forms: **Tuple Relational Calculus (TRC)**, where variables range over **tuples**, and **Domain Relational Calculus (DRC)**, where variables range over **attribute values (domains)**.

**2. Block Diagram**

```
                     +---------------------------+
                     |  Formal Query Languages   |
                     +-------------+-------------+
                                   |
              +--------------------+--------------------+
              |                                         |
   +----------v-----------+                 +-----------v------------+
   |  Procedural          |                 |  Non-Procedural        |
   |  Relational Algebra  |                 |  Relational Calculus   |
   +----------------------+                 +-----------+------------+
                                                        |
                                    +-------------------+------------------+
                                    |                                      |
                         +----------v-----------+               +----------v-----------+
                         |   Tuple RC (TRC)     |               |  Domain RC (DRC)     |
                         |  var = whole tuple   |               |  var = column value  |
                         |  {t | P(t)}          |               |  {<x1..xn>|P(x1..xn)}|
                         |  Basis of: SQL, QUEL |               |  Basis of: QBE       |
                         +----------------------+               +----------------------+
```

**3. Core Explanation / Working**

*Sample relation:* `STUDENT(Roll, Name, Age, Dept)`

*(a) Tuple Relational Calculus (TRC)*

- **General form:** `{ t | P(t) }`, read as "the set of all tuples t for which predicate P is true".
- `t.A` means the value of attribute A in tuple t.
- Uses `∈`, comparison operators (`<, >, =, ≠, ≤, ≥`), connectives (`∧, ∨, ¬, ⇒`) and quantifiers (`∃` there exists, `∀` for all).
- *Example 1:* names of students older than 20:
  `{ t.Name | t ∈ STUDENT ∧ t.Age > 20 }`
- *Example 2 (with a join):* names of students in the 'CSE' department, using `DEPT(Dept, HOD)`:
  `{ t.Name | t ∈ STUDENT ∧ ∃ d ∈ DEPT ( d.Dept = t.Dept ∧ d.Dept = 'CSE' ) }`

*(b) Domain Relational Calculus (DRC)*

- **General form:** `{ <x1, x2, ..., xn> | P(x1, x2, ..., xn) }`
- Each `xi` is a **domain variable** that stands for a single attribute value.
- `<r, n, a, d> ∈ STUDENT` means a tuple with those values exists in STUDENT.
- *Example 1:* names of students older than 20:
  `{ <n> | ∃ r, a, d ( <r, n, a, d> ∈ STUDENT ∧ a > 20 ) }`
- *Example 2:* roll number and name of CSE students:
  `{ <r, n> | ∃ a ( <r, n, a, 'CSE'> ∈ STUDENT ) }`

*(c) Safety of Expressions*

- An expression like `{ t | ¬(t ∈ STUDENT) }` is **unsafe** because it produces an infinite result.
- A **safe** expression only returns values from the **domain of the expression**, meaning values that appear in the relations or constants used in the query.
- Safe TRC, safe DRC and relational algebra have **equal expressive power**. This property is called **relational completeness**.

**4. Key Characteristics - TRC vs. DRC**

| Basis | Tuple Relational Calculus (TRC) | Domain Relational Calculus (DRC) |
|---|---|---|
| Variable represents | An entire **tuple** (row) | A single **attribute value** (column) |
| General syntax | `{ t \| P(t) }` | `{ <x1,...,xn> \| P(x1,...,xn) }` |
| Attribute access | Dot notation `t.Name` | Positional `<r, n, a, d>` |
| Membership test | `t ∈ R` | `<x1,...,xn> ∈ R` |
| Query language based on it | SQL, QUEL (Ingres) | QBE (Query-By-Example) |
| Readability | Easier for multi-attribute relations | Lengthy, since all columns must be listed |
| Expressive power | Same as relational algebra (safe expressions) | Same as relational algebra (safe expressions) |

**5. Advantages & Disadvantages**

*Advantages*

- It is **declarative**: users state *what* they want, which is close to natural logic.
- It allows **query optimization freedom**, because the DBMS chooses the execution strategy.
- It is **relationally complete**, with the same power as relational algebra.

*Disadvantages*

- Unsafe expressions can give **infinite results**, so safety checks are needed.
- Quantifiers (`∀`, `∃`) make complex queries **hard to write and understand** for beginners.
- Like basic algebra, it does not support aggregation directly.

**6. Conclusion / Application**

TRC is the theoretical basis of **SQL's** `SELECT ... FROM ... WHERE` and DRC is the basis of **QBE** interfaces like the MS Access query designer.

---

### Q3. Explain Domain constraints, Entity Integrity and Referential Integrity with table examples. (7 Marks)

**1. Introduction / Definition**

**Integrity constraints** are rules applied to a database to keep its data **accurate, valid and consistent**. They are defined in the schema (using DDL) and the DBMS **enforces them automatically** on every insert, update and delete.

**2. Block Diagram**

```
                   +------------------------------+
                   |     Integrity Constraints    |
                   +---------------+--------------+
                                   |
      +---------------+------------+-------------+------------------+
      |               |                          |                  |
+-----v------+  +-----v-------+        +---------v--------+  +------v------+
|  DOMAIN    |  |    KEY      |        |  ENTITY          |  | REFERENTIAL |
| Constraint |  | Constraint  |        |  INTEGRITY       |  |  INTEGRITY  |
+------------+  +-------------+        +------------------+  +-------------+
| Data type, |  | Uniqueness  |        | Primary key can  |  | FK value must|
| range,     |  | of candidate|        | never be NULL    |  | match a PK or|
| CHECK      |  | keys        |        |                  |  | be NULL      |
+------------+  +-------------+        +------------------+  +-------------+

   Referential link:
   STUDENT.Dept_ID (Foreign Key) ------references-----> DEPARTMENT.Dept_ID (Primary Key)
      (Referencing / Child)                               (Referenced / Parent)
```

**3. Core Explanation / Working**

*(a) Domain Constraint*

- Each attribute value must be an **atomic** value from its defined **domain** (data type, length, range, format).
- Defined using data types, `NOT NULL`, `DEFAULT` and `CHECK`.
- SQL: `Age INT CHECK (Age BETWEEN 17 AND 30)`

```
 STUDENT
 +------+-------+-------+
 | Roll | Name  |  Age  |
 +------+-------+-------+
 | 101  | Harsh |  21   |  <- Valid
 | 102  | Neha  | 'abc' |  <- VIOLATION: Age must be INT
 | 103  | Ravi  |  45   |  <- VIOLATION: CHECK (17-30) fails
 +------+-------+-------+
```

*(b) Key Constraint*

- Every candidate key must be **unique**. No two tuples may have the same key value.

*(c) Entity Integrity Constraint*

- **No primary key attribute may be NULL.** The primary key identifies each tuple uniquely, and NULL cannot identify anything.
- SQL: `Roll INT PRIMARY KEY` (this implies `NOT NULL` and `UNIQUE`).

```
 STUDENT
 +------+-------+
 | Roll | Name  |
 +------+-------+
 | 101  | Harsh |   <- Valid
 | NULL | Aman  |   <- VIOLATION: PK cannot be NULL
 | 101  | Priya |   <- VIOLATION: duplicate PK (key constraint)
 +------+-------+
```

*(d) Referential Integrity Constraint*

- A **foreign key (FK)** value in the referencing (child) table must either **match an existing primary key** value in the referenced (parent) table or be **NULL**.
- SQL: `Dept_ID INT REFERENCES DEPARTMENT(Dept_ID)`

```
 DEPARTMENT (Parent)          STUDENT (Child)
 +---------+-------+          +------+-------+---------+
 | Dept_ID | DName |          | Roll | Name  | Dept_ID |
 +---------+-------+          +------+-------+---------+
 |   10    | CSE   |<---------| 101  | Harsh |   10    |  Valid
 |   20    | IT    |<---------| 102  | Neha  |   20    |  Valid
 +---------+-------+          | 103  | Ravi  |  NULL   |  Valid (not assigned)
                              | 104  | Mohit |   50    |  VIOLATION: 50 not in parent
                              +------+-------+---------+
```

*(e) How operations can violate constraints*

- **Insert:** can violate domain, key, entity and referential integrity (child insert with a non-existent FK).
- **Delete:** can violate referential integrity only (deleting a parent row that child rows still reference).
- **Update:** can violate all of them.
- *Actions on violation:* `RESTRICT/NO ACTION` (reject), `CASCADE` (propagate), `SET NULL`, `SET DEFAULT`.

**4. Key Characteristics - Comparison**

| Basis | Domain Constraint | Entity Integrity | Referential Integrity |
|---|---|---|---|
| Applies to | Every attribute | Primary key attributes | Foreign key attributes |
| Rule | Value from valid domain | PK ≠ NULL | FK = some PK value or NULL |
| Scope | Single attribute | Single relation | Two relations |
| SQL syntax | Data type, CHECK, NOT NULL | PRIMARY KEY | FOREIGN KEY ... REFERENCES |
| Violated by | Insert, Update | Insert, Update | Insert (child), Delete (parent), Update |

**5. Advantages & Disadvantages**

*Advantages*

- They keep the database **accurate and consistent** by preventing invalid data.
- Enforcement is **centralised** in the DBMS, so each application does not need validation code.
- Referential integrity prevents **orphan records** (dangling references).

*Disadvantages*

- Checking constraints on every operation adds **performance overhead**, especially on bulk loads.
- `CASCADE` actions can **unintentionally delete** large amounts of related data.

**6. Conclusion / Application**

Integrity constraints are used in every **banking, e-commerce and university ERP** system. For example, an order row can never refer to a non-existent customer.

---

### Q4. Short Definitions (2 Marks Each)

**(a) Cartesian Product (×)**

- A binary operation that combines **every tuple of R with every tuple of S**.
- If R has m tuples and n1 attributes, and S has p tuples and n2 attributes, then R × S has **m x p tuples** and **n1 + n2 attributes**.
- Example: R with 3 rows × S with 4 rows = 12 rows.

**(b) Theta Join (⋈θ)**

- A join that combines tuples from two relations that satisfy a **general condition θ**, which can use any of `=, <, >, ≤, ≥, ≠`.
- `R ⋈θ S = σθ (R × S)`
- Example: `EMP ⋈ (EMP.Salary > MGR.Salary) MGR`. When θ uses only `=`, it is called an **Equi Join**.

**(c) Foreign Key and Cascading Deletes**

- When a foreign key is declared with **`ON DELETE CASCADE`**, deleting a parent (referenced) row **automatically deletes all child rows** that refer to it. This keeps referential integrity without leaving orphan rows.
- SQL: `FOREIGN KEY (Dept_ID) REFERENCES DEPARTMENT(Dept_ID) ON DELETE CASCADE`
- Example: deleting `Dept_ID = 10` from DEPARTMENT also deletes every STUDENT row with `Dept_ID = 10`.

---

## Unit 3: Database Design & Normalization

### Q1. Prove whether a given database decomposition is lossless or lossy, and explain dependency preservation. (7 Marks)

**1. Introduction / Definition**

A decomposition of relation R into R1 and R2 is **lossless (non-additive) join** if joining R1 and R2 gives back **exactly** the original R, with no extra (spurious) tuples: `R1 ⋈ R2 = R`. If the join produces spurious tuples, the decomposition is **lossy**. A decomposition is **dependency preserving** if every functional dependency of R can be checked using the decomposed relations alone.

**2. Flowchart - Lossless Join Test (Binary Decomposition)**

```
            +-----------------------------------+
            |  Given R, F and R1, R2            |
            +-----------------+-----------------+
                              |
            +-----------------v-----------------+
            | Cond 1: R1 ∪ R2 = R ?             |---- No ---> LOSSY
            +-----------------+-----------------+
                              | Yes
            +-----------------v-----------------+
            | Cond 2: R1 ∩ R2 ≠ ∅ ?             |---- No ---> LOSSY
            +-----------------+-----------------+
                              | Yes
            +-----------------v-----------------+
            | Compute (R1 ∩ R2)+ using F        |
            +-----------------+-----------------+
                              |
            +-----------------v-----------------+
            | Cond 3: (R1 ∩ R2) -> R1  OR       |---- No ---> LOSSY
            |         (R1 ∩ R2) -> R2 ?         |
            |  (common attr is a key of R1/R2)  |
            +-----------------+-----------------+
                              | Yes
                       +------v------+
                       |  LOSSLESS   |
                       +-------------+
```

**3. Core Explanation / Working**

*(a) Conditions for a lossless join (R into R1, R2)*

1. `Attr(R1) ∪ Attr(R2) = Attr(R)`
2. `Attr(R1) ∩ Attr(R2) ≠ ∅`
3. `R1 ∩ R2 → R1` **or** `R1 ∩ R2 → R2` must hold in F+. In other words, the common attribute(s) must be a **superkey** of at least one of the two relations.

*(b) Solved Example 1 - LOSSLESS*

`R(A, B, C, D, E)`, `F = { A → BC, CD → E, B → D, E → A }`
Decomposition: `R1(A, B, C)` and `R2(A, D, E)`

- Cond 1: {A,B,C} ∪ {A,D,E} = {A,B,C,D,E} = R. **Satisfied.**
- Cond 2: R1 ∩ R2 = {A} ≠ ∅. **Satisfied.**
- Cond 3: compute A+.
  - Start: A+ = {A}
  - A → BC gives {A, B, C}
  - B → D gives {A, B, C, D}
  - CD → E gives {A, B, C, D, E}
  - So A+ = ABCDE, and A → ABC (= R1) holds. **Satisfied.**
- **Result: the decomposition is LOSSLESS.**

*(c) Solved Example 2 - LOSSY (shown with data)*

`R(A, B, C)`, `F = { A → B }`, decomposed into `R1(A, B)` and `R2(B, C)`.

- R1 ∩ R2 = {B}, and B+ = {B}. B is a key of neither R1 nor R2, so the decomposition is **LOSSY**.

```
     R                  R1           R2           R1 ⋈ R2
 +---+---+---+       +---+---+    +---+---+    +---+---+---+
 | A | B | C |       | A | B |    | B | C |    | A | B | C |
 +---+---+---+       +---+---+    +---+---+    +---+---+---+
 | 1 | x | p |  -->  | 1 | x |    | x | p |    | 1 | x | p |
 | 2 | x | q |       | 2 | x |    | x | q |    | 1 | x | q | <- spurious
 +---+---+---+       +---+---+    +---+---+    | 2 | x | p | <- spurious
                                               | 2 | x | q |
                                               +---+---+---+
```

The join gives 4 tuples instead of 2. The extra tuples make information **ambiguous**, which is why the decomposition is called "lossy".

*(d) Decomposition into more than two relations (successive joins)*

- `R(A,B,C,D)`, `F = {A → B, B → C, C → D}`, decomposition `R1(A,B), R2(B,C), R3(C,D)`.
- R1 ⋈ R2: common attribute B, and B → C, so B is a key of R2. Lossless, giving `R12(A,B,C)`.
- R12 ⋈ R3: common attribute C, and C → D, so C is a key of R3. Lossless, giving `R(A,B,C,D)`.
- **Result: LOSSLESS.** For harder cases, use the **Chase (Tableau) matrix method**.

*(e) Dependency Preservation*

- Let Fi be the set of FDs in F+ that contain **only attributes of Ri** (the projection of F onto Ri).
- The decomposition is **dependency preserving** if `(F1 ∪ F2 ∪ ... ∪ Fn)+ = F+`.
- *Checking Example 1:*
  - F1 on R1(A,B,C): `A → BC` and `BC → A`. BC → A holds because BC+ = BCDEA.
  - F2 on R2(A,D,E): `A → DE` and `E → A`.
  - Is `B → D` implied by F1 ∪ F2? B+ = {B}, which does not contain D. **Not preserved.**
  - Is `CD → E` implied? CD+ = {C, D}, which does not contain E. **Not preserved.**
  - **Conclusion:** the decomposition in Example 1 is **lossless but NOT dependency preserving**.

**4. Key Characteristics - Lossless vs. Lossy / Dependency Preservation**

| Basis | Lossless Join | Lossy Join | Dependency Preservation |
|---|---|---|---|
| Join result | Exactly the original R | R plus spurious tuples | Not about the join |
| Test | Common attr is a key of R1 or R2 | Test fails | (∪ Fi)+ = F+ |
| Necessity | **Mandatory** | Never acceptable | Desirable (may be given up for BCNF) |
| Guaranteed by | 3NF and BCNF algorithms | - | 3NF synthesis (not always BCNF) |

**5. Advantages & Disadvantages**

*Advantages*

- A lossless decomposition **removes redundancy** without losing information.
- Dependency preservation lets constraints be **checked locally** on single tables without costly joins.
- Together they guarantee a **correct normalization** (3NF gives both properties).

*Disadvantages*

- A lossless decomposition still needs **joins** at query time, which costs performance.
- **BCNF may not preserve dependencies**, so a designer sometimes has to accept 3NF.

**6. Conclusion / Application**

The lossless-join test is used in **schema normalization tools** and by database designers to make sure that splitting tables (for example in an ERP schema) never corrupts the stored information.

---

### Q2. Calculate the minimal cover (canonical cover) for a given set of functional dependencies. (7 Marks)

**1. Introduction / Definition**

A **canonical (minimal) cover Fc** of an FD set F is the **smallest equivalent set** of FDs such that: (i) every FD has a **single attribute on the RHS**, (ii) no FD has an **extraneous attribute** on its LHS, and (iii) no FD is **redundant**. Fc has the same closure as F (`Fc+ = F+`).

**2. Flowchart - Algorithm**

```
        +-------------------------------------------+
        |              Given FD set F               |
        +---------------------+---------------------+
                              |
        +---------------------v---------------------+
        | STEP 1: Decompose RHS (singleton RHS)     |
        |   A -> BC  ==>  A -> B ,  A -> C          |
        +---------------------+---------------------+
                              |
        +---------------------v---------------------+
        | STEP 2: Remove extraneous LHS attributes  |
        |   For XY -> Z: if X+ contains Z, drop Y   |
        +---------------------+---------------------+
                              |
        +---------------------v---------------------+
        | STEP 3: Remove redundant FDs              |
        |   For X -> A: drop it, compute X+ with    |
        |   the rest; if A is in X+, it's redundant |
        +---------------------+---------------------+
                              |
        +---------------------v---------------------+
        | STEP 4: Union rule - combine same LHS     |
        |   A -> B , A -> C  ==>  A -> BC           |
        +---------------------+---------------------+
                              |
                     +--------v--------+
                     | Canonical Cover |
                     |       Fc        |
                     +-----------------+
```

**3. Core Explanation / Working - Solved Example 1**

**Given:** `F = { A → B, C → B, D → ABC, AC → D }`

*Step 1: Make every RHS a single attribute*

```
 F1 = { A → B,  C → B,  D → A,  D → B,  D → C,  AC → D }
```

*Step 2: Remove extraneous attributes from LHS* (only `AC → D` has a composite LHS)

- Is A extraneous? Check C+ = {C, B}. D is not in it, so **A is needed**.
- Is C extraneous? Check A+ = {A, B}. D is not in it, so **C is needed**.
- `AC → D` stays as it is.

*Step 3: Remove redundant FDs* (for each FD, compute the LHS closure without that FD)

| FD tested | Closure using the remaining FDs | RHS found? | Decision |
|---|---|---|---|
| A → B | A+ = {A} | No | Keep |
| C → B | C+ = {C} | No | Keep |
| D → A | D+ = {D, B, C} | No | Keep |
| D → B | D+ = {D, A, C, B} (via D→A, A→B) | **Yes** | **Remove** |
| D → C | D+ = {D, A, B} | No | Keep |
| AC → D | AC+ = {A, C, B} | No | Keep |

*Step 4: Combine FDs with the same LHS*

- `D → A` and `D → C` combine to give `D → AC`.

**Answer:**

```
   Fc = { A → B,  C → B,  D → AC,  AC → D }
```

**Solved Example 2 (Korth)**

**Given:** `F = { A → BC, B → C, A → B, AB → C }`

- *Step 1:* `{ A → B, A → C, B → C, A → B, AB → C }`. Remove the duplicate to get `{ A → B, A → C, B → C, AB → C }`.
- *Step 2:* in `AB → C`, A+ = {A, B, C} already contains C, so **B is extraneous**. `AB → C` becomes `A → C`, which is a duplicate.
- *Step 3:* `A → C` is redundant, because A → B and B → C give A → C by transitivity. Remove it.
- **Answer: `Fc = { A → B, B → C }`**

**4. Key Characteristics - F vs. Fc**

| Property | Original F | Canonical Cover Fc |
|---|---|---|
| RHS | May be composite | Single attribute (combined only at the end) |
| Extraneous attributes | May exist | None |
| Redundant FDs | May exist | None |
| Closure | F+ | Fc+ = F+ (equivalent) |
| Uniqueness | - | **Not unique**, since several minimal covers may exist |

**5. Advantages & Disadvantages**

*Advantages*

- It **reduces the cost of checking** FDs on every database update.
- It is the **input to the 3NF synthesis algorithm**, which gives a lossless and dependency-preserving design.
- It removes redundancy in the constraint set, making the design **simpler to analyse**.

*Disadvantages*

- Computing closures repeatedly is **time-consuming by hand** for large FD sets.
- The result is **not unique**: a different processing order may give a different (but equivalent) cover.

**6. Conclusion / Application**

The canonical cover is used by **database design tools** and in the **3NF decomposition algorithm** to produce optimal table structures with the fewest constraints to enforce.

---

### Q3. Explain Multivalued Dependency (MVD) leading to 4NF, followed by Join Dependency leading to 5NF. (7 Marks)

**1. Introduction / Definition**

A **Multivalued Dependency (MVD)** `X →→ Y` exists when, for one value of X, there is a **set of Y values that is independent** of the other attributes. **4NF** removes non-trivial MVDs. A **Join Dependency (JD)** exists when a relation can be rebuilt losslessly **only by joining three or more** of its projections. **5NF (PJNF)** removes such join dependencies.

**2. Block Diagram - Normal Form Hierarchy**

```
  +-----------------+
  | Unnormalized    |
  +--------+--------+
           | remove multi-valued / repeating attributes
  +--------v--------+
  |      1NF        |
  +--------+--------+
           | remove partial dependencies
  +--------v--------+
  |      2NF        |
  +--------+--------+
           | remove transitive dependencies
  +--------v--------+
  |      3NF        |
  +--------+--------+
           | every determinant must be a superkey
  +--------v--------+
  |      BCNF       |
  +--------+--------+
           | remove non-trivial MVDs           <-- Topic of this answer
  +--------v--------+
  |      4NF        |
  +--------+--------+
           | remove JDs not implied by keys    <-- Topic of this answer
  +--------v--------+
  |   5NF / PJNF    |
  +-----------------+
```

**3. Core Explanation / Working**

*(a) Multivalued Dependency (MVD)*

- **Definition:** in R, `X →→ Y` holds if whenever two tuples t1 and t2 agree on X, there exist tuples t3 and t4 such that:
  - t3[X] = t4[X] = t1[X] = t2[X]
  - t3[Y] = t1[Y] and t3[R−X−Y] = t2[R−X−Y]
  - t4[Y] = t2[Y] and t4[R−X−Y] = t1[R−X−Y]
- **Trivial MVD:** Y ⊆ X, or X ∪ Y = R.
- MVDs always occur in pairs: if `X →→ Y` then `X →→ (R − X − Y)` (the complementation rule).
- Every FD is also an MVD (if X → Y then X →→ Y).

*(b) Example - Relation with an MVD (in BCNF, but not 4NF)*

A student takes several courses and has several hobbies, and the two are **independent** of each other.

```
 STUDENT_INFO  (Key = {SID, Course, Hobby})
 +-----+--------+---------+
 | SID | Course |  Hobby  |
 +-----+--------+---------+
 | S1  | DBMS   | Cricket |
 | S1  | DBMS   | Music   |
 | S1  | OS     | Cricket |
 | S1  | OS     | Music   |
 +-----+--------+---------+
   MVDs:  SID →→ Course   and   SID →→ Hobby
```

- Problem: adding one new hobby for S1 requires **2 new rows** (one per course). This is redundancy and an update anomaly.

*(c) Fourth Normal Form (4NF)*

- **Definition:** R is in 4NF if it is in **BCNF** and, for every **non-trivial MVD** `X →→ Y`, **X is a superkey**.
- In the example, SID is not a superkey, so the relation is **not in 4NF**.
- **Decomposition:** for X →→ Y, split into R1(X ∪ Y) and R2(R − Y).

```
 STUDENT_COURSE              STUDENT_HOBBY
 +-----+--------+            +-----+---------+
 | SID | Course |            | SID |  Hobby  |
 +-----+--------+            +-----+---------+
 | S1  | DBMS   |            | S1  | Cricket |
 | S1  | OS     |            | S1  | Music   |
 +-----+--------+            +-----+---------+
   Both now in 4NF (only trivial MVDs remain). The decomposition is lossless.
```

*(d) Join Dependency (JD)*

- **Definition:** R satisfies the join dependency `*(R1, R2, ..., Rn)` if R is always equal to the natural join of its projections: `R = π R1 (R) ⋈ π R2 (R) ⋈ ... ⋈ π Rn (R)`.
- An MVD is a special case of a JD with n = 2.
- A JD is **trivial** if one of the Ri equals R.

*(e) Example - Relation with a JD (in 4NF, but not 5NF)*

Rule (cyclic constraint): if a Supplier supplies Part P, the Supplier supplies to Project J, and Project J uses Part P, then the Supplier supplies P to J.

```
 SPJ (all attributes form the key; no MVD exists)
 +----------+------+---------+
 | Supplier | Part | Project |
 +----------+------+---------+
 |    S1    |  P1  |   J2    |
 |    S1    |  P2  |   J1    |
 |    S2    |  P1  |   J1    |
 |    S1    |  P1  |   J1    |
 +----------+------+---------+
```

- Projections: `SP = {S1P1, S1P2, S2P1}`, `PJ = {P1J2, P2J1, P1J1}`, `JS = {J2S1, J1S1, J1S2}`.
- `SP ⋈ PJ` = {S1P1J2, S1P1J1, S1P2J1, **S2P1J2**, S2P1J1}. The tuple S2P1J2 is **spurious**, so 2 projections are not enough.
- `(SP ⋈ PJ) ⋈ JS` removes S2P1J2, because (J2, S2) is not in JS. The result is exactly SPJ.
- So `*(SP, PJ, JS)` holds and is **not implied by the candidate key**.

*(f) Fifth Normal Form (5NF / Project-Join Normal Form)*

- **Definition:** R is in 5NF if it is in 4NF and **every non-trivial join dependency is implied by the candidate keys**.
- **Decomposition:** replace SPJ with the three tables `SP(Supplier, Part)`, `PJ(Part, Project)` and `JS(Project, Supplier)`. Each one is in 5NF.

**4. Key Characteristics - 4NF vs. 5NF**

| Basis | 4NF | 5NF (PJNF) |
|---|---|---|
| Dependency removed | Multivalued dependency (MVD) | Join dependency (JD) |
| Pre-condition | Must be in BCNF | Must be in 4NF |
| Condition | For every non-trivial X →→ Y, X is a superkey | Every JD is implied by candidate keys |
| Decomposed into | 2 relations | 3 or more relations |
| Typical cause | Independent multi-valued facts | Cyclic constraint among 3+ entities |
| Example | SID, Course, Hobby | Supplier, Part, Project |

**5. Advantages & Disadvantages**

*Advantages*

- They **remove the redundancy** caused by independent multi-valued facts, which BCNF cannot remove.
- They eliminate **insertion, deletion and update anomalies** completely.
- 5NF is the **ultimate normal form** for project-join decomposition: the data cannot be decomposed any further without loss.

*Disadvantages*

- More tables means **more joins** and slower query performance.
- JDs are **hard to identify** in real schemas, so 5NF is rarely applied in practice.

**6. Conclusion / Application**

4NF and 5NF are applied in **data-warehouse staging and complex supply-chain systems**, where independent multi-valued facts (Supplier-Part-Project) would otherwise create huge redundancy.

---

### Q4. Short Definitions (2 Marks Each)

**(a) Update / Insertion Anomalies**

- **Insertion anomaly:** a fact cannot be inserted without inserting other, unrelated facts. Example: a new department cannot be added until at least one student joins it, if both are stored in one table.
- **Update anomaly:** a change to one fact must be repeated in many rows. If one row is missed, the data becomes **inconsistent**. Example: a department's HOD name stored in every student row.
- (**Deletion anomaly:** deleting one fact unintentionally deletes another, for example deleting the last student also deletes the department details.)

**(b) Trivial vs. Non-Trivial Functional Dependency**

| Trivial FD | Non-Trivial FD |
|---|---|
| `X → Y` where **Y ⊆ X** | `X → Y` where **Y ⊄ X** |
| Always holds, so it carries no information | Gives real information about the data |
| Example: `{Roll, Name} → Name` | Example: `Roll → Name` |

- *Completely non-trivial:* `X ∩ Y = ∅`.

**(c) Armstrong's Axioms** (sound and complete inference rules for FDs)

- **Reflexivity:** if Y ⊆ X, then X → Y.
- **Augmentation:** if X → Y, then XZ → YZ.
- **Transitivity:** if X → Y and Y → Z, then X → Z.
- *Derived rules:* **Union** (X → Y, X → Z gives X → YZ), **Decomposition** (X → YZ gives X → Y and X → Z), **Pseudo-transitivity** (X → Y, WY → Z gives WX → Z).

---

## Unit 4: Transactions & Concurrency Control

### Q1. Differentiate between conflict and view serializability, and test a given schedule for view serializability. (7 Marks)

**1. Introduction / Definition**

A schedule is **serializable** if its effect is equivalent to some **serial schedule**. **Conflict serializability** requires that the schedule can be turned into a serial one by **swapping non-conflicting operations**. **View serializability** only requires that the schedule gives every transaction the **same "view"** (the same reads and the same final writes) as a serial schedule.

**2. Flowchart - Testing a Schedule**

```
            +-----------------------------------+
            |          Given Schedule S         |
            +-----------------+-----------------+
                              |
            +-----------------v-----------------+
            | Draw precedence graph (conflicts: |
            |   R-W, W-R, W-W on same item)     |
            +-----------------+-----------------+
                              |
                    +---------v---------+
                    |  Cycle in graph?  |
                    +----+---------+----+
                      No |         | Yes
          +--------------v--+   +--v-------------------------+
          | CONFLICT        |   | Not conflict serializable. |
          | SERIALIZABLE    |   | Any BLIND WRITE in S?      |
          | => also VIEW    |   +--+----------------------+--+
          | SERIALIZABLE    |      | No                   | Yes
          +-----------------+   +--v--------------+   +---v-----------------------+
                                | NOT VIEW        |   | Check view equivalence    |
                                | SERIALIZABLE    |   | with each serial order:   |
                                +-----------------+   | 1. Initial read           |
                                                      | 2. Updated (W-R) read     |
                                                      | 3. Final write            |
                                                      +---+-----------------------+
                                                          |
                                                 Match found => VIEW SERIALIZABLE
```

**3. Core Explanation / Working**

*(a) Conflict Serializability*

- Two operations **conflict** if they belong to **different transactions**, act on the **same data item**, and **at least one is a write**: R-W, W-R or W-W.
- **Test:** build a **precedence graph**. Draw an edge Ti → Tj if an operation of Ti conflicts with, and comes before, an operation of Tj.
- If the graph is **acyclic**, the schedule is conflict serializable. A topological sort gives the equivalent serial order.

*(b) View Serializability*

- Schedules S and S' are **view equivalent** if, for each data item Q:
  1. **Initial read:** if Ti reads the initial value of Q in S, it also reads the initial value in S'.
  2. **Updated read (reads-from):** if Ti reads a value of Q written by Tj in S, it does so in S' as well.
  3. **Final write:** the transaction that performs the last write on Q in S also does so in S'.
- S is **view serializable** if it is view equivalent to some serial schedule.
- Every conflict-serializable schedule is view serializable, but **not the other way round**. The extra view-serializable schedules always contain **blind writes** (writes without a preceding read).
- Testing view serializability is **NP-complete**.

*(c) Solved Example - Test for View Serializability*

```
 Schedule S:
 +---------+---------+---------+
 |   T1    |   T2    |   T3    |
 +---------+---------+---------+
 | R(A)    |         |         |
 |         | W(A)    |         |
 | W(A)    |         |         |
 |         |         | W(A)    |
 +---------+---------+---------+
```

*Step 1: Conflict test with a precedence graph*

- R1(A) before W2(A) gives T1 → T2.
- W2(A) before W1(A) gives T2 → T1.
- W1(A) before W3(A) gives T1 → T3. W2(A) before W3(A) gives T2 → T3.

```
         +------+   T1 -> T2   +------+
         |  T1  |------------->|  T2  |
         |      |<-------------|      |
         +--+---+   T2 -> T1   +--+---+
            |                     |
            +--------+   +--------+
                     v   v
                   +------+
                   |  T3  |
                   +------+
   Cycle T1 -> T2 -> T1 exists  ==>  NOT conflict serializable
```

*Step 2: View test.* W2(A) and W3(A) are **blind writes**, so check against the serial order T1 → T2 → T3.

| Condition | Schedule S | Serial T1 → T2 → T3 | Match? |
|---|---|---|---|
| Initial read of A | T1 | T1 | Yes |
| Updated (W-R) reads | None | None | Yes |
| Final write of A | T3 | T3 | Yes |

- **Result:** S is view equivalent to T1 → T2 → T3, so S is **VIEW SERIALIZABLE** but **not conflict serializable**.

**4. Key Characteristics - Conflict vs. View Serializability**

| Basis | Conflict Serializability | View Serializability |
|---|---|---|
| Based on | Order of conflicting operations | Initial read, reads-from, final write |
| Test | Precedence graph (acyclic) | View equivalence with serial schedules |
| Complexity | Polynomial (easy) | **NP-complete** (hard) |
| Blind writes | Not considered specially | Allow extra schedules with blind writes |
| Relationship | Subset (stricter) | Superset (more permissive) |
| Used in practice | Yes (2PL, timestamps) | Mostly theoretical |

**5. Advantages & Disadvantages**

*Advantages*

- Both guarantee **database consistency** while still allowing **concurrent execution**.
- The conflict test is **efficient** and is the basis of practical protocols like 2PL.
- View serializability **accepts more schedules**, which allows more concurrency in theory.

*Disadvantages*

- Testing view serializability is **NP-complete**, so it is not practical for a real DBMS.
- Conflict serializability **rejects some correct schedules** (those with blind writes).

**6. Conclusion / Application**

Serializability theory is the **correctness criterion** behind every concurrency-control protocol used in RDBMSs like Oracle and PostgreSQL. Conflict serializability is the form actually enforced.

---

### Q2. Explain the Timestamp Ordering Protocol and how the Thomas Write Rule handles obsolete write operations. (7 Marks)

**1. Introduction / Definition**

The **Timestamp Ordering (TO) Protocol** is a **non-lock-based** concurrency control method. It gives each transaction a unique **timestamp TS(Ti)** when it starts, and makes sure conflicting operations run in **timestamp order**, so the schedule is equivalent to the serial order of the timestamps. The **Thomas Write Rule** is a modification that **ignores obsolete writes** instead of rolling the transaction back.

**2. Flowchart - Basic TO Protocol with Thomas Write Rule**

```
                       +------------------------+
                       | Ti issues an operation |
                       |      on item Q         |
                       +-----------+------------+
                                   |
                 +-----------------+------------------+
                 |                                    |
          +------v------+                      +------v------+
          |   READ(Q)   |                      |  WRITE(Q)   |
          +------+------+                      +------+------+
                 |                                    |
     +-----------v-----------+           +------------v-----------+
     | TS(Ti) < W-TS(Q) ?    |           | TS(Ti) < R-TS(Q) ?     |
     +----+-------------+----+           +----+--------------+----+
      Yes |             | No              Yes |              | No
   +------v-----+  +----v-----------+  +------v-----+  +-----v-----------------+
   | REJECT,    |  | EXECUTE read;  |  | REJECT,    |  | TS(Ti) < W-TS(Q) ?    |
   | rollback Ti|  | R-TS(Q) =      |  | rollback Ti|  +----+-------------+----+
   +------------+  | max(R-TS,TS(Ti)|  +------------+   Yes |             | No
                   +----------------+          +----------v--------+ +--v-------------+
                                               | Basic TO: ROLLBACK| | EXECUTE write; |
                                               | Thomas: IGNORE    | | W-TS(Q)=TS(Ti) |
                                               | write (obsolete)  | +----------------+
                                               +-------------------+
```

**3. Core Explanation / Working**

*(a) Timestamps*

- **TS(Ti):** a unique timestamp given when Ti starts (from the system clock or a logical counter). If Ti starts before Tj, then TS(Ti) < TS(Tj).
- **W-timestamp(Q):** the largest timestamp of any transaction that **wrote** Q successfully.
- **R-timestamp(Q):** the largest timestamp of any transaction that **read** Q successfully.

*(b) Rules of the Basic Timestamp Ordering Protocol*

- **When Ti issues READ(Q):**
  - If `TS(Ti) < W-TS(Q)`, Ti wants a value that has already been overwritten by a younger transaction. **Reject and roll back Ti.**
  - Otherwise, **execute** the read and set `R-TS(Q) = max(R-TS(Q), TS(Ti))`.
- **When Ti issues WRITE(Q):**
  - If `TS(Ti) < R-TS(Q)`, a younger transaction has already read the old value. **Reject and roll back Ti.**
  - If `TS(Ti) < W-TS(Q)`, Ti is trying to write an **obsolete** value. **Reject and roll back Ti.**
  - Otherwise, **execute** the write and set `W-TS(Q) = TS(Ti)`.
- A rolled-back transaction restarts with a **new, larger timestamp**.

*(c) Thomas Write Rule*

- It changes **only the second write check**.
- If `TS(Ti) < W-TS(Q)`, the write is **obsolete**, because a younger transaction has already written Q and nobody will ever read Ti's value. So the write is simply **ignored** and Ti continues, with no rollback.
- This allows some **view-serializable schedules that are not conflict serializable**, which increases concurrency.

*(d) Solved Example*

TS(T1) = 10, TS(T2) = 20, and initially R-TS(Q) = W-TS(Q) = 0.

| Step | Operation | Check | Basic TO | Thomas Write Rule |
|---|---|---|---|---|
| 1 | R1(Q) | 10 ≥ W-TS = 0 | Execute, R-TS(Q) = 10 | Execute, R-TS(Q) = 10 |
| 2 | W2(Q) | 20 ≥ R-TS = 10, 20 ≥ W-TS = 0 | Execute, W-TS(Q) = 20 | Execute, W-TS(Q) = 20 |
| 3 | W1(Q) | 10 ≥ R-TS = 10, but 10 < W-TS = 20 | **Rollback T1** | **Ignore W1(Q)**, T1 continues |

**4. Key Characteristics - Basic TO vs. Thomas Write Rule**

| Basis | Basic Timestamp Ordering | Thomas Write Rule |
|---|---|---|
| Obsolete write (TS(Ti) < W-TS(Q)) | Rollback Ti | Ignore the write |
| Schedules allowed | Conflict serializable only | Also some view serializable |
| Concurrency | Lower | Higher |
| Number of rollbacks | More | Fewer |
| Deadlock | Free (no locks) | Free (no locks) |

**5. Advantages & Disadvantages**

*Advantages*

- It is **deadlock-free**, because no transaction ever waits for a lock.
- It guarantees **serializability** in timestamp order.
- The Thomas Write Rule **reduces unnecessary rollbacks**, which improves throughput.

*Disadvantages*

- **Starvation** is possible, because a long transaction may be rolled back again and again.
- The schedules may be **non-recoverable** or cause **cascading rollbacks** unless strict TO is used.
- Storing R-TS and W-TS for every data item and updating them on each access adds **overhead**.

**6. Conclusion / Application**

Timestamp-based concurrency control is the basis of **MVCC (Multi-Version Concurrency Control)** used in PostgreSQL, Oracle and distributed databases like Google Spanner.

---

### Q3. Explain multiple granularity locking, lock escalation and the purpose of intention lock modes. (7 Marks)

**1. Introduction / Definition**

**Multiple granularity locking (MGL)** lets a transaction lock data items of **different sizes** (database, area, file, record), arranged as a **tree hierarchy**. A lock on a node **implicitly locks all its descendants**. **Intention locks** (IS, IX, SIX) are placed on ancestor nodes to show that **finer-level locks are held** below them.

**2. Block Diagram - Granularity Hierarchy Tree**

```
                              +------+
   Level 0 (Coarsest)         |  DB  |
                              +--+---+
                    +------------+-------------+
                 +--v--+                    +--v--+
   Level 1       | A1  |    (Areas)         | A2  |
                 +--+--+                    +--+--+
             +------+-----+              +-----+------+
          +--v--+      +--v--+        +--v--+      +--v--+
   Level 2|Fa   |      |Fb   |        |Fc   |      |Fd   |  (Files/Tables)
          +--+--+      +--+--+        +--+--+      +--+--+
           /   \        /   \          /   \        /   \
   Level 3 ra1 ra2    rb1  rb2       rc1  rc2     rd1  rd2  (Records / Rows)
   (Finest)

   Locking: TOP-DOWN (root first)      Unlocking: BOTTOM-UP (leaf first)
```

**3. Core Explanation / Working**

*(a) Lock Modes*

- **S (Shared):** read access to the node and all its descendants.
- **X (Exclusive):** read/write access to the node and all its descendants.
- **IS (Intention-Shared):** explicit S locks will be taken at a **lower level**.
- **IX (Intention-Exclusive):** explicit X or S locks will be taken at a **lower level**.
- **SIX (Shared + Intention-Exclusive):** the whole subtree is locked in S mode, and some lower nodes will get X locks. Example: read a whole table and update a few rows.

*(b) Compatibility Matrix* (Y = compatible, N = conflict)

```
 +---------+------+------+------+------+------+
 | Held -> |  IS  |  IX  |  S   | SIX  |  X   |
 +---------+------+------+------+------+------+
 |   IS    |  Y   |  Y   |  Y   |  Y   |  N   |
 |   IX    |  Y   |  Y   |  N   |  N   |  N   |
 |   S     |  Y   |  N   |  Y   |  N   |  N   |
 |   SIX   |  Y   |  N   |  N   |  N   |  N   |
 |   X     |  N   |  N   |  N   |  N   |  N   |
 +---------+------+------+------+------+------+
```

*(c) Rules of the Multiple Granularity Locking Protocol* (for transaction Ti)

1. Ti must follow the **compatibility matrix**.
2. The **root** must be locked first, in any mode.
3. Ti can lock node Q in **S or IS** mode only if it holds the **parent** in **IX or IS** mode.
4. Ti can lock node Q in **X, SIX or IX** mode only if it holds the **parent** in **IX or SIX** mode.
5. Ti follows **two-phase locking**: it cannot lock any node after it has unlocked one.
6. Ti can **unlock** Q only if it holds **no locks on any child** of Q.

*Example:* T1 wants to update record `ra1`. It takes **IX** on DB, **IX** on A1, **IX** on Fa and then **X** on ra1. At the same time, T2 can read `rb1` by taking IS on DB, IS on A1, IS on Fb and S on rb1. Both run in parallel because IX and IS are compatible.

*(d) Purpose of Intention Locks*

- Without them, to lock a whole file the DBMS would have to **search every descendant** to check for conflicting locks, which is very slow.
- With intention locks, the DBMS only checks the **node and its ancestors**. If any ancestor shows a conflicting intention, the request waits.
- This lets **coarse and fine locks coexist** safely and efficiently.

*(e) Lock Escalation*

- When a transaction holds **too many fine-grained locks** (for example more than 5000 row locks on one table), the DBMS **replaces them with one coarser lock** (a table lock).
- **Why:** it reduces **memory use** for the lock table and the **overhead of lock management**.
- **Cost:** concurrency drops, because other transactions are now blocked from the whole table.
- Used in **SQL Server and DB2** (escalation from row to page to table).

**4. Key Characteristics - Fine vs. Coarse Granularity**

| Basis | Fine Granularity (Record) | Coarse Granularity (Table/DB) |
|---|---|---|
| Concurrency | **High** | Low |
| Locking overhead | High (many locks) | **Low** (few locks) |
| Lock table memory | Large | Small |
| Best for | Short transactions on few rows | Long transactions scanning whole tables |
| Deadlock chance | Higher | Lower |

**5. Advantages & Disadvantages**

*Advantages*

- It **balances concurrency and overhead** by choosing the right lock size for each transaction.
- Intention locks make conflict detection **fast**, since there is no need to scan the subtree.
- It ensures **serializability**, because it is based on two-phase locking.

*Disadvantages*

- It is **complex to implement**, with five lock modes and hierarchical rules.
- **Deadlocks are still possible**, because the protocol is lock-based.
- Lock escalation can suddenly **reduce concurrency** and cause blocking.

**6. Conclusion / Application**

Multiple granularity locking with intention locks is implemented in **Microsoft SQL Server, IBM DB2 and MySQL InnoDB** (IS/IX table-level intention locks with row locks).

---

### Q4. Short Definitions (2 Marks Each)

**(a) Dirty Read Problem (Temporary Update / W-R Conflict)**

- Happens when a transaction **reads data written by another transaction that has not yet committed**. If that transaction then **aborts**, the first transaction has used an invalid value.
- Example: T1 writes A = 500 (uncommitted), T2 reads A = 500, then T1 rolls back, so T2 holds a "dirty" value.

**(b) Unrepeatable Read Problem (R-W Conflict)**

- Happens when a transaction **reads the same item twice and gets different values**, because another transaction **modified and committed** it between the two reads.
- Example: T1 reads A = 100, T2 updates A = 200 and commits, then T1 reads A again and gets 200.

**(c) Starvation vs. Deadlock**

| Starvation | Deadlock |
|---|---|
| A transaction **waits indefinitely** while others keep proceeding | Two or more transactions **wait for each other in a cycle**, so none can proceed |
| Caused by an unfair scheduling or victim-selection policy | Caused by circular wait on locks |
| Other transactions are progressing | The involved transactions are all blocked |
| Fix: aging, FIFO lock queue | Fix: prevention (wait-die, wound-wait), detection (wait-for graph) and recovery |

---

## Unit 5: Recovery & File Organization

### Q1. Explain the shadow paging database recovery technique along with its primary advantages and disadvantages. (7 Marks)

**1. Introduction / Definition**

**Shadow paging** is a recovery technique that **does not need a log** (in a single-user environment). The database is divided into fixed-size **pages**, and two page tables are kept during a transaction: the **current page table** and the **shadow page table**. The shadow table is never changed during the transaction, so it always points to the last consistent state.

**2. Block Diagram**

```
   +----------------------+                      +----------------------+
   |  SHADOW PAGE TABLE   |                      |  CURRENT PAGE TABLE  |
   |  (on disk, frozen)   |                      |  (in memory, live)   |
   +------+---------------+     DISK PAGES       +------+---------------+
   | Page | Points to     |   +--------------+   | Page | Points to     |
   +------+---------------+   | P1  (old)    |   +------+---------------+
   |  1   | P1            |   | P2  (old)    |   |  1   | P1   (shared) |
   |  2   | P2            |   | P3  (old)    |   |  2   | P2'  (NEW)    |
   |  3   | P3            |   | P4  (old)    |   |  3   | P3   (shared) |
   |  4   | P4            |   | P2' (copy)   |   |  4   | P4'  (NEW)    |
   +------+---------------+   | P4' (copy)   |   +------+---------------+
              ^               +--------------+              ^
              |                                             |
              |     +----------------------------------+    |
              +-----|  DB ROOT POINTER (fixed address) |----+
           (before  +----------------------------------+  (after commit:
            commit)                                        atomic switch)

   Abort / crash  -> root still points to SHADOW table -> old consistent state
   Commit         -> root switched to CURRENT table   -> new state is durable
```

**3. Core Explanation / Working**

- **Step 1 - Start of transaction:** the current page table is **copied** to make the shadow page table, which is saved to stable storage. Both point to the same disk pages.
- **Step 2 - Read operation:** pages are found through the **current page table**.
- **Step 3 - Write operation (copy-on-write):**
  - Find a **free page** on disk.
  - Copy the old page into the free page and apply the update to this **new copy**.
  - Change the **current page table** entry to point to the new page.
  - The shadow page table still points to the **old, unchanged** page.
- **Step 4 - Commit:**
  1. Write all modified data pages to disk.
  2. Write the current page table to disk.
  3. **Atomically** change the fixed **DB root pointer** from the shadow table to the current table. This single disk write is the commit point.
- **Step 5 - Abort / crash recovery:**
  - Discard the current page table and the new pages.
  - The root pointer still points to the **shadow table**, which reflects the consistent state from before the transaction.
  - **No UNDO and no REDO** is needed. Free the unused pages (garbage collection).

**4. Key Characteristics - Shadow Paging vs. Log-Based Recovery**

| Basis | Shadow Paging | Log-Based Recovery |
|---|---|---|
| Log required | No (single user) | Yes |
| Recovery operations | None (NO-UNDO / NO-REDO) | UNDO and/or REDO |
| Recovery speed | Very fast | Slower (log scanning) |
| Commit overhead | High (copy page table, flush pages) | Low (flush log records) |
| Data locality | Destroyed (pages scattered) | Preserved |
| Concurrency support | Difficult | Easy |

**5. Advantages & Disadvantages**

*Advantages*

- **No log overhead** in a single-user environment.
- **Very fast recovery**, because no undo or redo is needed. Reverting to the shadow table is enough.
- Simple **atomic commit** using a single pointer switch.

*Disadvantages*

- **Commit overhead:** the entire page table must be written at commit, which is costly for large databases.
- **Data fragmentation:** updated pages move to new locations, so related pages are no longer **contiguous**.
- **Garbage collection** is needed to reclaim old pages after commit.
- Hard to extend to **concurrent transactions**, where logs and checkpoints are still needed.

**6. Conclusion / Application**

Shadow paging is used in **System R (early IBM RDBMS)**, the **SQLite rollback journal concept**, and modern **copy-on-write file systems** like ZFS and Btrfs.

---

### Q2. Explain Checkpointing. Differentiate between deferred and immediate database modification with log records. (7 Marks)

**1. Introduction / Definition**

**Log-based recovery** keeps a **log** (a sequential file in stable storage) of every database modification, so the system can **UNDO** or **REDO** transactions after a failure. A **checkpoint** is a point at which the DBMS writes all buffers to disk and records `<checkpoint>` in the log. This limits how much of the log must be scanned during recovery.

**2. Block Diagram - Checkpoint Recovery Timeline**

```
  Time ------------------------------------------------------------------->
                           Tc (Checkpoint)                 Tf (Crash)
                                 |                              |
  T1  |=========|                |                              |  -> Ignore (done before Tc)
  T2        |====================|=========|                    |  -> REDO (committed after Tc)
  T3              |==============|==============================X  -> UNDO (not committed)
  T4                             |  |==============|            |  -> REDO (committed)
  T5                             |          |===================X  -> UNDO (not committed)
                                 |                              |
            |=====| = transaction duration     X = still active at crash
```

**3. Core Explanation / Working**

*(a) Log Record Types*

- `<Ti start>`: transaction Ti has started.
- `<Ti, X, V_old, V_new>`: Ti changed item X from V_old to V_new.
- `<Ti commit>`: Ti has committed.
- `<Ti abort>`: Ti has aborted.

*(b) Deferred Database Modification (NO-UNDO / REDO)*

- All writes are **postponed until the transaction commits**. They are recorded only in the log and a local buffer.
- Log records hold **only the new value**: `<Ti, X, V_new>`.
- After `<Ti commit>` is written to the log, the updates are applied to the database.
- **Recovery:** REDO(Ti) if the log has both `<Ti start>` and `<Ti commit>`. Otherwise ignore Ti. **UNDO is never needed.**

*(c) Immediate Database Modification (UNDO / REDO)*

- Writes may be applied to the database **before the transaction commits**, as long as the log record is written first (the WAL rule).
- Log records hold **both old and new values**: `<Ti, X, V_old, V_new>`.
- **Recovery:**
  - **UNDO(Ti)** if the log has `<Ti start>` but no `<Ti commit>`. Restore the old values, scanning **backward**.
  - **REDO(Ti)** if the log has both `<Ti start>` and `<Ti commit>`. Reapply the new values, scanning **forward**.

*(d) Example* - T0: A = 1000 to 950, B = 2000 to 2050. T1: C = 700 to 600.

```
   DEFERRED MODIFICATION LOG         IMMEDIATE MODIFICATION LOG
   +--------------------------+      +------------------------------+
   | <T0 start>               |      | <T0 start>                   |
   | <T0, A, 950>             |      | <T0, A, 1000, 950>           |
   | <T0, B, 2050>            |      | <T0, B, 2000, 2050>          |
   | <T0 commit>              |      | <T0 commit>                  |
   | <T1 start>               |      | <T1 start>                   |
   | <T1, C, 600>             |      | <T1, C, 700, 600>            |
   |   --- CRASH ---          |      |   --- CRASH ---              |
   +--------------------------+      +------------------------------+
   Recovery: REDO(T0);               Recovery: REDO(T0);
             ignore T1                         UNDO(T1) -> C = 700
```

*(e) Checkpointing*

- **Problem without checkpoints:** the whole log must be scanned, and many already-saved transactions get redone needlessly.
- **Steps to take a checkpoint:**
  1. Write all log records in main memory to **stable storage**.
  2. Write all **modified buffer blocks** to disk.
  3. Write a `<checkpoint L>` record to the log, where L is the list of active transactions.
- **Recovery using a checkpoint:**
  - Scan backward to the last `<checkpoint L>`.
  - Only transactions in L, or those that started after the checkpoint, are considered.
  - Committed ones go into the **redo-list**. Uncommitted ones go into the **undo-list**.
  - Transactions that committed **before** the checkpoint are **ignored** (T1 in the diagram).

**4. Key Characteristics - Deferred vs. Immediate Modification**

| Basis | Deferred Modification | Immediate Modification |
|---|---|---|
| When DB is updated | Only after commit | Before or after commit |
| Log record format | `<Ti, X, V_new>` | `<Ti, X, V_old, V_new>` |
| Recovery operations | **REDO only** (NO-UNDO) | **UNDO and REDO** |
| Old value needed | No | Yes |
| Buffer requirement | Large (holds all updates) | Small |
| Concurrency | Lower | Higher |
| Commit speed | Slower (all writes happen at commit) | Faster |

**5. Advantages & Disadvantages**

*Advantages*

- Logs make sure the **Atomicity and Durability** properties of ACID survive crashes.
- Checkpoints **reduce recovery time** sharply by limiting the log scan.
- Deferred modification is **simple** (no undo). Immediate modification gives **better performance** and concurrency.

*Disadvantages*

- Log writing adds **I/O overhead** to every update.
- Taking a checkpoint **briefly pauses** transaction processing (unless fuzzy checkpoints are used).
- Deferred modification needs **large buffers** for long transactions.

**6. Conclusion / Application**

Immediate modification with checkpoints is the basis of **ARIES**, the recovery algorithm used in **IBM DB2, SQL Server and PostgreSQL (WAL)**.

---

### Q3. Compare B-Trees and B+ Trees. Demonstrate step-by-step insertion in a B-Tree of order m. (7 Marks)

**1. Introduction / Definition**

A **B-Tree of order m** is a **self-balancing multi-way search tree** in which every node has at most **m children** and **m − 1 keys**, every non-root node has at least **⌈m/2⌉ children**, and **all leaves are at the same level**. A **B+ Tree** is a variant in which **all data records are stored only in leaf nodes**, internal nodes hold only index keys, and the leaves are **linked sequentially**.

**2. Block Diagram - Structure Comparison**

```
  B-TREE (order 3): data pointers in ALL nodes

                     +---------+
                     |   40*   |            * = key + data pointer
                     +--+---+--+
                +-------+   +-------+
           +----v----+         +----v----+
           |   20*   |         |   60*   |
           +-+-----+-+         +-+-----+-+
             |     |             |     |
          +--v-+ +-v--+       +--v-+ +-v--+
          |10* | |30* |       |50* | |70* |
          +----+ +----+       +----+ +----+

  B+ TREE (order 3): data only at LEAVES, leaves linked

                         +---------+
                         |   40    |        (index keys only)
                         +--+---+--+
                  +---------+   +---------+
             +----v----+           +----v----+
             |   20    |           |   60    |
             +--+---+--+           +--+---+--+
          +-----+   +----+       +----+   +----+
       +--v--+     +-----v-+  +--v----+  +----v--+
       | 10* |---->| 20*30*|->| 40*50*|->| 60*70*|-> NULL
       +-----+     +-------+  +-------+  +-------+
                 (sequential linked list of leaves)
```

**3. Core Explanation / Working**

*(a) Properties of a B-Tree of order m*

- Every node has at most **m children** and **m − 1 keys**.
- Every internal node (except the root) has at least **⌈m/2⌉ children**, that is **⌈m/2⌉ − 1 keys**.
- The root has at least **2 children** (if it is not a leaf).
- All leaves are at the **same depth**, so the tree is perfectly balanced.
- The keys in each node are kept in **sorted order**.

*(b) Insertion Algorithm*

1. Search for the correct **leaf** node for the new key.
2. If the leaf has fewer than m − 1 keys, **insert in sorted order**. Done.
3. If the leaf **overflows** (it now has m keys), **split** it:
   - The **median key moves up** to the parent.
   - The left half and the right half become two separate nodes.
4. If the parent overflows too, split it recursively. If the **root splits**, a new root is created and the **height increases by 1**.

*(c) Solved Example - Insert 10, 20, 30, 40, 50, 60, 70 into a B-Tree of order m = 3* (max 2 keys per node)

```
 Step 1: Insert 10            Step 2: Insert 20
         [10]                         [10 | 20]

 Step 3: Insert 30  -> [10 | 20 | 30] OVERFLOW -> split, median 20 goes up
                 [20]
                /    \
             [10]    [30]

 Step 4: Insert 40  -> goes to leaf [30]
                 [20]
                /    \
             [10]    [30 | 40]

 Step 5: Insert 50  -> [30 | 40 | 50] OVERFLOW -> split, median 40 goes up
                 [20 | 40]
                /    |    \
             [10]  [30]   [50]

 Step 6: Insert 60  -> goes to leaf [50]
                 [20 | 40]
                /    |    \
             [10]  [30]   [50 | 60]

 Step 7: Insert 70  -> [50 | 60 | 70] OVERFLOW -> 60 goes up
         Root becomes [20 | 40 | 60] OVERFLOW -> split root, 40 goes up

                       [40]                 <- New root (height +1)
                     /      \
                 [20]        [60]
                /    \      /    \
             [10]   [30]  [50]   [70]
```

*Final tree:* height = 3, all leaves at the same level, and every node has between 1 and 2 keys.

**4. Key Characteristics - B-Tree vs. B+ Tree**

| Basis | B-Tree | B+ Tree |
|---|---|---|
| Data pointers stored in | All nodes (internal + leaf) | **Leaf nodes only** |
| Duplicate keys | No, each key appears once | Yes, keys repeat in internal nodes |
| Leaf linking | Leaves not linked | Leaves form a **linked list** |
| Search time | Variable (may end at an internal node) | Uniform (always reaches a leaf) |
| Range / sequential queries | Slow (tree traversal) | **Fast** (follow leaf links) |
| Fan-out of internal nodes | Lower (data pointers take space) | **Higher**, so the tree is shorter |
| Deletion | Complex (from internal nodes) | Simpler (always from a leaf) |
| Usage | Some file systems | **Almost all DBMS indexes** |

**5. Advantages & Disadvantages**

*Advantages*

- **Balanced height**, so search, insert and delete take **O(log n)** time.
- **Few disk I/Os**, because large nodes match disk block size.
- The B+ Tree supports **efficient range queries and sequential access**.

*Disadvantages*

- Insertions and deletions need **splits and merges**, which are complex to implement.
- Nodes may be only **half full**, which wastes space.
- The B+ Tree stores keys **twice** (in internal nodes and leaves).

**6. Conclusion / Application**

B+ Trees are the **default index structure** in MySQL InnoDB, Oracle, PostgreSQL and SQL Server. B-Trees are used in file systems like NTFS and HFS+.

---

### Q4. Short Definitions (2 Marks Each)

**(a) Write-Ahead Logging (WAL)**

- A rule that says **the log record for a change must be written to stable storage before** the changed data page is written to disk.
- In addition, all log records of a transaction, including `<Ti commit>`, must be on stable storage **before the transaction is declared committed**.
- This makes **UNDO and REDO** possible after a crash. It is used in PostgreSQL, SQLite and others.

**(b) Static vs. Dynamic Hashing**

| Static Hashing | Dynamic Hashing |
|---|---|
| The **number of buckets is fixed** in advance | Buckets **grow and shrink** as data changes |
| Overflow is handled by **overflow chains** | Overflow is handled by **splitting buckets** |
| Performance falls as the database grows | Performance stays stable |
| Example: `h(K) = K mod 10` | Example: **Extendible hashing**, Linear hashing |

**(c) Primary vs. Clustering vs. Secondary Index**

- **Primary index:** built on the **ordering key field** (primary key) of a **sorted** file. It is **sparse**, with one entry per block. There is only one per file.
- **Clustering index:** built on an **ordering non-key field** (which can repeat) of a sorted file. There is one entry per **distinct value**.
- **Secondary index:** built on a **non-ordering field**. The file is not sorted on this field, so the index must be **dense**. A file can have **many** secondary indexes.

---

# Web Technology (BCS-502)

---

## Unit 1: Web Foundations, HTML & XML

### Q1. Short Definitions (2 Marks Each)

**(a) Define HTTP and mention its three basic features.**

- **HTTP (HyperText Transfer Protocol)** is an **application-layer, request-response protocol** used to transfer hypertext (HTML, images, data) between a web **client (browser)** and a **web server**. It runs over TCP, on **port 80** by default (HTTPS uses port 443).
- **Three basic features:**
  1. **Connectionless:** the client sends a request, the server responds, and the connection is closed. A new connection is used for the next request (in HTTP/1.0).
  2. **Stateless:** the server keeps **no memory** of previous requests. Each request is independent, so cookies and sessions are used to keep state.
  3. **Media independent:** any type of data (text, image, video, JSON) can be sent, as long as both sides understand the **MIME type** given in the `Content-Type` header.

**(b) Differentiate between HTML and XML.**

| Basis | HTML | XML |
|---|---|---|
| Full form | HyperText Markup Language | eXtensible Markup Language |
| Purpose | **Displays** data (presentation) | **Stores and transports** data |
| Tags | **Predefined** (`<p>`, `<h1>`) | **User-defined** (`<book>`, `<author>`) |
| Case sensitivity | Not case sensitive | **Case sensitive** |
| Closing tags | Some optional (`<br>`, `<li>`) | **Mandatory** for every element |
| Error handling | Lenient (browser ignores errors) | **Strict** (must be well-formed) |
| Whitespace | Not preserved | Preserved |

**(c) Difference between Client-Server and Peer-to-Peer paradigms.**

| Client-Server | Peer-to-Peer (P2P) |
|---|---|
| A **dedicated server** provides services and clients request them | **Every node (peer)** acts as both client and server |
| **Centralised** control and data | **Decentralised**, with data distributed among peers |
| The server is a **single point of failure** | **No single point of failure** |
| Easy to secure and back up | Hard to secure and manage |
| Costly (needs server hardware) | Cheap (uses peers' resources) |
| Example: Web (browser to Apache), email | Example: BitTorrent, blockchain, Skype (early) |

---

### Q2. Explain web development strategies and the web development process using a block diagram. (7 Marks)

**1. Introduction / Definition**

**Web development** is the process of building, testing and maintaining websites and web applications. A **web development strategy** is the planned approach (goals, audience, technology and methodology) followed to deliver a site that is **usable, scalable and secure**. The **web development process** is the step-by-step life cycle from planning to maintenance.

**2. Block Diagram - Web Development Life Cycle**

```
   +------------------------------+
   | 1. Information Gathering /   |  Goals, target audience, purpose
   |    Requirement Analysis      |
   +--------------+---------------+
                  |
   +--------------v---------------+
   | 2. Planning                  |  Sitemap, technology stack,
   |    (Sitemap & Wireframe)     |  wireframes, timeline
   +--------------+---------------+
                  |
   +--------------v---------------+
   | 3. Design                    |  UI/UX, layout, colour,
   |    (Mock-ups / Prototype)    |  typography, client review
   +--------------+---------------+
                  |
   +--------------v---------------+
   | 4. Content Writing &         |  Text, images, SEO keywords
   |    Assembly                  |
   +--------------+---------------+
                  |
   +--------------v---------------+       +---------------------+
   | 5. Development (Coding)      |<----->| Front end: HTML,    |
   |                              |       | CSS, JavaScript     |
   +--------------+---------------+       | Back end: Node/JSP, |
                  |                       | DB: MySQL/MongoDB   |
   +--------------v---------------+       +---------------------+
   | 6. Testing & Review          |  Functional, cross-browser,
   |                              |  performance, security tests
   +--------------+---------------+
                  |       ^  bugs found
                  |       +-------------- back to step 5
   +--------------v---------------+
   | 7. Deployment / Launch       |  Hosting, domain, upload (FTP/CI)
   +--------------+---------------+
                  |
   +--------------v---------------+
   | 8. Maintenance & Updates     |  Monitoring, backups, new features
   +------------------------------+
```

**3. Core Explanation / Working**

*(a) Web Development Strategies*

- **Define goals and audience:** decide what the site must achieve (sales, information, service) and for whom.
- **Choose an architecture:** a static site, a dynamic site (server-side rendering), or a **single-page application (SPA)**.
- **Mobile-first / responsive design:** design for small screens first, then scale up with CSS media queries.
- **Choose a methodology:**
  - **Waterfall:** sequential phases, suited to fixed requirements.
  - **Agile / Scrum:** short iterative sprints with frequent client feedback.
  - **Rapid prototyping:** build a quick model, take feedback, refine.
- **Technology stack selection:** for example **MERN** (MongoDB, Express, React, Node) or **LAMP** (Linux, Apache, MySQL, PHP).
- **SEO, accessibility and security** are planned from the start, not added at the end.

*(b) Web Development Process (as in the diagram)*

1. **Information gathering:** understand the purpose, the audience and the content needed.
2. **Planning:** build a **sitemap** (page hierarchy) and **wireframes** (page skeletons). Choose tools.
3. **Design:** create the visual layout and UI mock-ups, and get approval.
4. **Content creation:** write text, collect media, optimise for SEO.
5. **Development:** code the front end (HTML, CSS, JS) and the back end (server logic, database, APIs).
6. **Testing:** check links, forms, browser compatibility, responsiveness, load and security.
7. **Deployment:** upload to a web server or cloud, and configure the domain and SSL.
8. **Maintenance:** fix bugs, update content and monitor performance.

**4. Key Characteristics - Waterfall vs. Agile Strategy**

| Basis | Waterfall | Agile |
|---|---|---|
| Flow | Linear, sequential | Iterative, incremental |
| Client feedback | At the end | After every sprint |
| Change handling | Difficult and costly | Easy |
| Delivery | One final release | Frequent working releases |
| Best for | Small, fixed-scope sites | Large, evolving web apps |

**5. Advantages & Disadvantages** (of following a structured process)

*Advantages*

- **Clear planning** reduces cost overruns and missed deadlines.
- Early testing gives a **higher-quality**, bug-free product.
- A responsive, SEO-friendly design improves **user reach**.

*Disadvantages*

- A structured process takes **more time** at the start (planning, documentation).
- With Waterfall, **late requirement changes** are expensive.

**6. Conclusion / Application**

This process is followed by every web agency and product team, for example when building an **e-commerce site like Flipkart** or a **college ERP portal**.

---

### Q3. Write the HTML code to create a comprehensive user registration form (using various input types and action attributes). (7 Marks)

**1. Introduction / Definition**

An **HTML form** collects user input and sends it to a server for processing. It is created with the `<form>` element. The **`action`** attribute gives the **URL** that will process the data, and the **`method`** attribute (`GET` or `POST`) decides **how** the data is sent.

**2. Block Diagram - Form Layout and Data Flow**

```
  +-----------------------------------------------+
  |           USER REGISTRATION FORM              |
  +-----------------------------------------------+
  | Full Name     : [ text            ]           |
  | Email         : [ email           ]           |
  | Password      : [ password        ]           |
  | Date of Birth : [ date            ]           |
  | Mobile        : [ tel             ]           |
  | Gender        : (o) Male  ( ) Female ( ) Other|  <- radio
  | Course        : [ B.Tech CSE   v ]            |  <- select
  | Skills        : [x] HTML [ ] CSS [x] JS       |  <- checkbox
  | Photo         : [ Choose File ]               |  <- file
  | Address       : [ textarea               ]    |
  |                 [                        ]    |
  | [x] I agree to the terms                      |
  |          [ Register ]   [ Reset ]             |  <- submit / reset
  +-----------------------+-----------------------+
                          | method="POST"
                          v action="/register"
             +--------------------------+
             |  Web Server (Servlet/    |
             |  Node.js) processes data |
             +--------------------------+
```

**3. Core Explanation / Working - HTML Code**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>User Registration</title>
</head>
<body>
  <h2>User Registration Form</h2>

  <form action="/register" method="post" enctype="multipart/form-data">
    <fieldset>
      <legend>Personal Details</legend>

      <label for="name">Full Name:</label>
      <input type="text" id="name" name="fullname"
             placeholder="Enter full name" maxlength="50" required><br><br>

      <label for="email">Email:</label>
      <input type="email" id="email" name="email" required><br><br>

      <label for="pwd">Password:</label>
      <input type="password" id="pwd" name="password"
             minlength="8" required><br><br>

      <label for="dob">Date of Birth:</label>
      <input type="date" id="dob" name="dob"><br><br>

      <label for="mob">Mobile:</label>
      <input type="tel" id="mob" name="mobile"
             pattern="[0-9]{10}" title="10-digit number"><br><br>

      <label for="age">Age:</label>
      <input type="number" id="age" name="age" min="17" max="60"><br><br>

      Gender:
      <input type="radio" id="m" name="gender" value="male" checked>
      <label for="m">Male</label>
      <input type="radio" id="f" name="gender" value="female">
      <label for="f">Female</label>
      <input type="radio" id="o" name="gender" value="other">
      <label for="o">Other</label><br><br>
    </fieldset>

    <fieldset>
      <legend>Academic Details</legend>

      <label for="course">Course:</label>
      <select id="course" name="course">
        <option value="cse">B.Tech CSE</option>
        <option value="it">B.Tech IT</option>
        <option value="ece">B.Tech ECE</option>
      </select><br><br>

      Skills:
      <input type="checkbox" name="skills" value="html"> HTML
      <input type="checkbox" name="skills" value="css"> CSS
      <input type="checkbox" name="skills" value="js"> JavaScript<br><br>

      <label for="photo">Upload Photo:</label>
      <input type="file" id="photo" name="photo" accept="image/*"><br><br>

      <label for="site">Portfolio URL:</label>
      <input type="url" id="site" name="website"><br><br>

      <label for="addr">Address:</label><br>
      <textarea id="addr" name="address" rows="4" cols="40"></textarea><br><br>

      <input type="hidden" name="source" value="college_portal">
      <input type="checkbox" id="agree" name="agree" required>
      <label for="agree">I agree to the terms and conditions</label><br><br>
    </fieldset>

    <input type="submit" value="Register">
    <input type="reset" value="Reset">
  </form>
</body>
</html>
```

*Explanation of the key attributes*

- `action="/register"`: the server URL that receives the form data.
- `method="post"`: sends the data in the **request body**, which is secure for passwords. `get` would append it to the URL.
- `enctype="multipart/form-data"`: **required** for file uploads.
- `name`: the key under which each value is sent (for example `email=abc@x.com`).
- `required`, `pattern`, `min`, `max`, `maxlength`: built-in **HTML5 validation**.
- `<fieldset>` and `<legend>` group related fields. `<label for>` links a label to its input.

**4. Key Characteristics - Input Types Used**

| Input Type | Purpose | Built-in Validation |
|---|---|---|
| `text` | Single-line text | maxlength, pattern |
| `email` | Email address | Checks the @ format |
| `password` | Hidden characters | minlength |
| `date` | Date picker | Valid date |
| `tel` | Phone number | pattern |
| `number` | Numeric input | min, max |
| `radio` | Choose one option | Same `name` groups them |
| `checkbox` | Choose many options | - |
| `file` | Upload file | accept |
| `url` | Web address | Checks URL format |
| `hidden` | Value sent without display | - |
| `submit` / `reset` | Send / clear the form | - |

**5. Advantages & Disadvantages**

*Advantages*

- HTML5 input types give **built-in validation** and suitable keyboards on mobile.
- Forms are a **standard, browser-independent** way to collect user data.
- `POST` with `multipart/form-data` supports **secure and binary (file)** submissions.

*Disadvantages*

- Client-side validation can be **bypassed**, so server-side validation is still required.
- Older browsers may **not support** newer input types like `date`.

**6. Conclusion / Application**

Registration forms like this are used on every **sign-up page**, for example college admission portals, Gmail sign-up and e-commerce account creation.

---

### Q4. Write an XML file to store library book information and design a valid XML DTD or XML Schema for it. (7 Marks)

**1. Introduction / Definition**

**XML (eXtensible Markup Language)** stores and transports data in a **self-describing, hierarchical** format with user-defined tags. A **DTD (Document Type Definition)** or an **XML Schema (XSD)** defines the **legal structure** of an XML document: its elements, attributes, order and data types. A document that follows its DTD or XSD is called **valid**.

**2. Block Diagram - XML Tree Structure**

```
                      +-----------+
                      |  library  |   (root element)
                      +-----+-----+
               +------------+-------------+
          +----v----+                +----v----+
          |  book   | id="B101"      |  book   | id="B102"
          +----+----+ category=...   +----+----+
     +-------+-+------+------+--------+
     |       |        |      |        |
  +--v--+ +--v---+ +--v--+ +-v---+ +--v-----+
  |title| |author| |isbn | |year | | price  |
  +-----+ +------+ +-----+ +-----+ +--------+

   XML file ---> validated against ---> DTD / XSD ---> "Valid XML"
```

**3. Core Explanation / Working**

*(a) XML File: `library.xml`* (with an internal DTD)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE library [
  <!ELEMENT library (book+)>
  <!ELEMENT book (title, author+, publisher, isbn, year, price, copies)>
  <!ELEMENT title     (#PCDATA)>
  <!ELEMENT author    (#PCDATA)>
  <!ELEMENT publisher (#PCDATA)>
  <!ELEMENT isbn      (#PCDATA)>
  <!ELEMENT year      (#PCDATA)>
  <!ELEMENT price     (#PCDATA)>
  <!ELEMENT copies    (#PCDATA)>
  <!ATTLIST book id       ID    #REQUIRED
                 category CDATA #IMPLIED>
  <!ATTLIST price currency CDATA "INR">
]>
<library>
  <book id="B101" category="Database">
    <title>Database System Concepts</title>
    <author>Abraham Silberschatz</author>
    <author>Henry F. Korth</author>
    <publisher>McGraw Hill</publisher>
    <isbn>9780073523323</isbn>
    <year>2019</year>
    <price currency="INR">850</price>
    <copies>12</copies>
  </book>
  <book id="B102" category="Web">
    <title>Web Technologies</title>
    <author>Uttam K. Roy</author>
    <publisher>Oxford</publisher>
    <isbn>9780198066224</isbn>
    <year>2018</year>
    <price currency="INR">560</price>
    <copies>8</copies>
  </book>
</library>
```

*DTD symbols used*

- `book+`: one or more book elements. (`*` means zero or more, `?` means zero or one.)
- `#PCDATA`: parsed character data (text).
- `ID #REQUIRED`: a unique, mandatory attribute. `#IMPLIED` means optional. `"INR"` is the default value.

*(b) Equivalent XML Schema: `library.xsd`*

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
  <xs:element name="library">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="book" maxOccurs="unbounded">
          <xs:complexType>
            <xs:sequence>
              <xs:element name="title"     type="xs:string"/>
              <xs:element name="author"    type="xs:string" maxOccurs="unbounded"/>
              <xs:element name="publisher" type="xs:string"/>
              <xs:element name="isbn"      type="xs:string"/>
              <xs:element name="year"      type="xs:gYear"/>
              <xs:element name="price">
                <xs:complexType>
                  <xs:simpleContent>
                    <xs:extension base="xs:decimal">
                      <xs:attribute name="currency" type="xs:string" default="INR"/>
                    </xs:extension>
                  </xs:simpleContent>
                </xs:complexType>
              </xs:element>
              <xs:element name="copies" type="xs:nonNegativeInteger"/>
            </xs:sequence>
            <xs:attribute name="id"       type="xs:ID"     use="required"/>
            <xs:attribute name="category" type="xs:string" use="optional"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>
</xs:schema>
```

*Linking the XSD to the XML file (instead of the internal DTD):*

```xml
<library xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:noNamespaceSchemaLocation="library.xsd">
```

**4. Key Characteristics - DTD vs. XML Schema**

| Basis | DTD | XML Schema (XSD) |
|---|---|---|
| Syntax | Non-XML (special syntax) | Written **in XML** itself |
| Data types | Only text (#PCDATA, CDATA) | **44+ built-in types** (int, date, decimal) |
| Namespaces | Not supported | Supported |
| Occurrence control | `?`, `*`, `+` only | `minOccurs`, `maxOccurs` (exact numbers) |
| Extensibility | Not extensible | Extensible (inheritance of types) |
| Complexity | Simple | More verbose and complex |

**5. Advantages & Disadvantages**

*Advantages (of XML with DTD/XSD)*

- **Platform independent**, so data can be exchanged between different systems.
- **Validation** catches structural errors before processing.
- **Self-describing** and human readable.

*Disadvantages*

- **Verbose**: the tags make files large compared with JSON.
- Parsing and validation need **extra processing time**.

**6. Conclusion / Application**

XML with schemas is used in **library management systems, SOAP web services, Android layouts and configuration files** (for example `web.xml` in Java web applications).

---

## Unit 2: Cascading Style Sheets (CSS)

### Q1. Short Definitions (2 Marks Each)

**(a) Three different ways to integrate CSS**

1. **Inline CSS:** written in the `style` attribute of an individual HTML element. It has the **highest priority**.
   `<p style="color: blue; font-size: 16px;">Hello</p>`
2. **Internal (Embedded) CSS:** written inside a `<style>` tag in the `<head>` section. It applies to **one page**.
   ```html
   <head>
     <style> p { color: blue; } </style>
   </head>
   ```
3. **External CSS:** written in a separate `.css` file and linked with `<link>`. It applies to **many pages** and is the best for maintenance.
   `<link rel="stylesheet" href="style.css">`
- **Priority (cascade):** Inline > Internal / External (whichever comes later in the code) > Browser default.

**(b) CSS syntax to remove the underline from a hyperlink**

```css
a {
    text-decoration: none;
}
/* Optional: show the underline again only on hover */
a:hover {
    text-decoration: underline;
}
```

---

### Q2. Illustrate the CSS Box Model with a proper block diagram, explaining margins, borders, padding and content. (7 Marks)

**1. Introduction / Definition**

The **CSS Box Model** says that **every HTML element is a rectangular box** made of four layers: **content, padding, border and margin**, from the inside out. It decides the **size, spacing and layout** of elements on a web page.

**2. Block Diagram**

```
 +-------------------------------------------------------------+
 |                        MARGIN (transparent)                 |
 |     +-----------------------------------------------+       |
 |     |                BORDER (visible line)          |       |
 |     |     +-----------------------------------+     |       |
 |     |     |      PADDING (takes background)   |     |       |
 |     |     |     +-----------------------+     |     |       |
 |     |     |     |                       |     |     |       |
 |     |     |     |        CONTENT        |     |     |       |
 |     |     |     |   (text / image)      |     |     |       |
 |     |     |     |   width x height      |     |     |       |
 |     |     |     |                       |     |     |       |
 |     |     |     +-----------------------+     |     |       |
 |     |     |                                   |     |       |
 |     |     +-----------------------------------+     |       |
 |     |                                               |       |
 |     +-----------------------------------------------+       |
 |                                                             |
 +-------------------------------------------------------------+
   Outside  <------------------------------------------>  Inside
   Margin  ->  Border  ->  Padding  ->  Content
```

**3. Core Explanation / Working**

- **Content:**
  - The innermost area, where text, images or child elements are shown.
  - Its size is set by `width` and `height`.
- **Padding:**
  - The space **between the content and the border**.
  - It is **transparent but shows the element's background colour**.
  - Properties: `padding-top`, `padding-right`, `padding-bottom`, `padding-left`, or the shorthand `padding: 10px 20px;`.
- **Border:**
  - The line that wraps around the padding and content.
  - Properties: `border-width`, `border-style` (solid, dashed, dotted), `border-color`, or the shorthand `border: 2px solid black;`.
- **Margin:**
  - The outermost space, **between this element and its neighbours**.
  - It is **fully transparent** (no background).
  - It can be **negative**, and `margin: auto` centres a block horizontally.
  - **Margin collapsing:** the vertical margins of adjacent block elements merge into the larger of the two.

*Example and size calculation*

```css
div {
    width: 300px;
    height: 100px;
    padding: 20px;
    border: 5px solid black;
    margin: 30px;
}
```

- **Total width** = width + left/right padding + left/right border + left/right margin
  = 300 + 2(20) + 2(5) + 2(30) = **410 px**
- **Total height** = 100 + 2(20) + 2(5) + 2(30) = **210 px**

*The `box-sizing` property*

- `box-sizing: content-box` (default): `width` covers the content only.
- `box-sizing: border-box`: `width` includes **content + padding + border**, so the box stays at the declared width. This makes responsive layouts easier.

**4. Key Characteristics - Padding vs. Margin**

| Basis | Padding | Margin |
|---|---|---|
| Position | Inside the border | Outside the border |
| Background | Shows element background | Always transparent |
| Negative values | Not allowed | Allowed |
| Collapsing | Never collapses | Vertical margins collapse |
| Click area | Part of the element | Not part of the element |
| Use | Space inside the box | Space between boxes |

**5. Advantages & Disadvantages**

*Advantages*

- Gives **precise control** over element size and spacing.
- Applies **uniformly to all elements**, so layouts are predictable.
- `border-box` makes **responsive design** simpler.

*Disadvantages*

- With the default `content-box`, total size calculations can **confuse beginners** (the declared width is not the real width).
- **Margin collapsing** can cause unexpected gaps.

**6. Conclusion / Application**

The box model is the **foundation of every CSS layout**, including Flexbox and Grid, and is used to design cards, buttons and page sections on all websites.

---

### Q3. Explain CSS positioning properties (static, relative, absolute, fixed) in detail. (7 Marks)

**1. Introduction / Definition**

The CSS **`position`** property decides **how an element is placed** in the document. It works together with the **offset properties** `top`, `right`, `bottom` and `left`. The main values are **static, relative, absolute and fixed** (and `sticky` in CSS3).

**2. Block Diagram**

```
 VIEWPORT (browser window)
 +-------------------------------------------------------------+
 |  [FIXED]  <- stays here even when the page scrolls          |
 |                                                             |
 |  +------------- Parent (position: relative) -------------+  |
 |  |                                                       |  |
 |  |  [ static box 1 ]   <- normal flow                    |  |
 |  |                                                       |  |
 |  |  [ static box 2 ]                                     |  |
 |  |         [ RELATIVE box ]  <- moved from its own       |  |
 |  |  .....  (gap left where it originally was)            |  |
 |  |                                       +------------+  |  |
 |  |  [ static box 3 ]                     | ABSOLUTE   |  |  |
 |  |                                       | top:10px;  |  |  |
 |  |                                       | right:10px |  |  |
 |  |                                       +------------+  |  |
 |  |       ^ removed from flow, placed relative to parent  |  |
 |  +-------------------------------------------------------+  |
 +-------------------------------------------------------------+
```

**3. Core Explanation / Working**

*(a) `position: static`* (default)

- The element follows the **normal document flow** (top to bottom, left to right).
- `top`, `left`, `right`, `bottom` and `z-index` have **no effect**.

```css
p { position: static; }
```

*(b) `position: relative`*

- The element is positioned **relative to its own normal position**.
- The offset moves the element, but its **original space is kept** (other elements do not move into the gap).
- Often used as a **container (reference point)** for absolutely positioned children.

```css
.box { position: relative; top: 20px; left: 30px; }
/* moves 20px down and 30px right from where it would normally be */
```

*(c) `position: absolute`*

- The element is **removed from the normal flow**. Other elements act as if it does not exist.
- It is placed relative to its **nearest positioned ancestor** (an ancestor that is not static). If there is none, it is placed relative to the `<html>` element (initial containing block).
- It **scrolls with the page**.

```css
.parent { position: relative; }
.badge  { position: absolute; top: 10px; right: 10px; }
```

*(d) `position: fixed`*

- **Removed from the normal flow** and positioned relative to the **browser viewport**.
- It **does not move** when the page is scrolled.
- Used for sticky headers, "back to top" buttons and chat widgets.

```css
.navbar { position: fixed; top: 0; left: 0; width: 100%; }
```

*(e) `position: sticky`* (CSS3, extra marks)

- Acts as **relative** until a scroll threshold is reached, then acts as **fixed**.
  `th { position: sticky; top: 0; }`

*(f) `z-index`*

- Controls the **stacking order** of positioned elements. A higher value appears in front.

**4. Key Characteristics - Comparison**

| Property | In normal flow? | Positioned relative to | Scrolls with page? | Offsets work? |
|---|---|---|---|---|
| static | Yes | Normal flow | Yes | No |
| relative | Yes (space kept) | Its own normal position | Yes | Yes |
| absolute | **No** | Nearest positioned ancestor | Yes | Yes |
| fixed | **No** | **Viewport** | **No** | Yes |
| sticky | Yes | Scroll container (threshold) | Until threshold | Yes |

**5. Advantages & Disadvantages**

*Advantages*

- Gives **precise placement** of elements like tooltips, badges and modals.
- `fixed` keeps **important navigation always visible**.
- `relative` combined with `absolute` makes building **overlay components** easy.

*Disadvantages*

- Absolute and fixed elements are **removed from the flow**, so they can **overlap** other content.
- Too much positioning makes layouts **hard to keep responsive**. Flexbox and Grid are better for page layout.

**6. Conclusion / Application**

Positioning is used for **fixed navigation bars, dropdown menus, notification badges, modal pop-ups and sticky table headers** on modern websites.

---

### Q4. Discuss different types of CSS selectors and pseudo-classes with examples. (7 Marks)

**1. Introduction / Definition**

A **CSS selector** is a pattern that **selects the HTML elements** to which a style rule applies. A **pseudo-class** is a keyword added to a selector (with a single colon `:`) that selects elements in a **special state** (like `:hover`) or **position** (like `:first-child`).

**2. Block Diagram - Classification of Selectors**

```
                         +------------------+
                         |  CSS SELECTORS   |
                         +--------+---------+
        +-----------+-----------+-+---------+-------------+--------------+
        |           |           |           |             |              |
   +----v----+ +----v----+ +----v----+ +----v-----+ +-----v-----+ +------v------+
   | Simple  | |Combinator| |Attribute| | Pseudo-  | |  Pseudo-  | |  Grouping / |
   |         | |          | |         | | class    | |  element  | |  Universal  |
   +---------+ +----------+ +---------+ +----------+ +-----------+ +-------------+
   | element | | A B      | | [type]  | | :hover   | | ::before  | |  *          |
   | .class  | | A > B    | | [a="v"] | | :focus   | | ::after   | |  h1, h2, p  |
   | #id     | | A + B    | | [a^="v"]| | :nth-    | | ::first-  | |             |
   |         | | A ~ B    | |         | |  child() | |   letter  | |             |
   +---------+ +----------+ +---------+ +----------+ +-----------+ +-------------+
```

**3. Core Explanation / Working**

*(a) Simple (Basic) Selectors*

- **Universal selector (`*`):** selects all elements.
  `* { margin: 0; padding: 0; }`
- **Element (type) selector:** selects all elements of one type.
  `p { color: gray; }`
- **Class selector (`.`):** selects elements with a given class. It can be reused on many elements.
  `.highlight { background: yellow; }`, used as `<p class="highlight">`
- **ID selector (`#`):** selects the **one unique** element with that id.
  `#header { height: 60px; }`, used as `<div id="header">`
- **Grouping selector (`,`):** applies the same style to several selectors.
  `h1, h2, h3 { font-family: Arial; }`

*(b) Combinator Selectors*

- **Descendant (`A B`):** any B inside A. `div p { color: blue; }`
- **Child (`A > B`):** only direct children. `ul > li { list-style: square; }`
- **Adjacent sibling (`A + B`):** the B immediately after A. `h1 + p { font-weight: bold; }`
- **General sibling (`A ~ B`):** every B after A with the same parent. `h1 ~ p { color: green; }`

*(c) Attribute Selectors*

- `[type]`: elements that have the attribute.
- `input[type="text"]`: the attribute equals a value.
- `a[href^="https"]`: the value **starts with**.
- `a[href$=".pdf"]`: the value **ends with**.
- `img[alt*="logo"]`: the value **contains**.

*(d) Pseudo-classes (single colon `:`)*

| Pseudo-class | Selects | Example |
|---|---|---|
| `:link` | Unvisited link | `a:link { color: blue; }` |
| `:visited` | Visited link | `a:visited { color: purple; }` |
| `:hover` | Element under the mouse | `a:hover { color: red; }` |
| `:active` | Element being clicked | `a:active { color: orange; }` |
| `:focus` | Element with keyboard focus | `input:focus { border: 2px solid blue; }` |
| `:first-child` | First child of its parent | `li:first-child { font-weight: bold; }` |
| `:last-child` | Last child | `li:last-child { border: none; }` |
| `:nth-child(n)` | The nth child | `tr:nth-child(even) { background: #eee; }` |
| `:not(sel)` | Elements not matching sel | `p:not(.intro) { font-size: 14px; }` |
| `:checked` | Checked checkbox/radio | `input:checked + label { color: green; }` |

- **LVHA order rule:** link styles must be written in the order `:link`, `:visited`, `:hover`, `:active`, or they will override each other.

*(e) Pseudo-elements (double colon `::`)*

- `p::first-letter { font-size: 200%; }`
- `p::first-line { font-weight: bold; }`
- `h2::before { content: "> "; }` and `h2::after { content: " <"; }`
- `::selection { background: yellow; }`

*(f) Specificity (which rule wins)*

- **Inline (1000) > ID (100) > Class / attribute / pseudo-class (10) > Element / pseudo-element (1)**. `!important` overrides all of these.

**4. Key Characteristics - Class vs. ID Selector, Pseudo-class vs. Pseudo-element**

| Basis | Class Selector | ID Selector |
|---|---|---|
| Symbol | `.` | `#` |
| Reusability | Many elements | One element per page |
| Specificity | 10 | 100 |

| Basis | Pseudo-class | Pseudo-element |
|---|---|---|
| Syntax | Single colon `:hover` | Double colon `::before` |
| Targets | A **state** of an existing element | A **part** of an element, or generated content |
| Example | `:focus`, `:nth-child()` | `::first-letter`, `::after` |

**5. Advantages & Disadvantages**

*Advantages*

- Selectors give **fine-grained targeting** without adding classes to every element.
- Pseudo-classes add **interactivity** (hover, focus) **without JavaScript**.
- Grouping and reusable classes **reduce code repetition**.

*Disadvantages*

- Complex selectors and specificity conflicts make CSS **hard to debug**.
- Deep descendant selectors are **slower to match** and fragile when the HTML structure changes.

**6. Conclusion / Application**

Selectors and pseudo-classes are used in every stylesheet, for example **zebra-striped tables (`:nth-child`), hover effects on navigation menus, and focus highlights on form fields**.

---

## Unit 3: JavaScript, AJAX & Networking

### Q1. Short Definitions (2 Marks Each)

**(a) What is AJAX and what is its primary advantage for dynamic webpages?**

- **AJAX (Asynchronous JavaScript And XML)** is a technique that uses the **`XMLHttpRequest` object (or the `fetch()` API)** to exchange data with the server **in the background**, without reloading the whole web page. The data can be XML, JSON or plain text.
- **Primary advantage:** **partial page update**. Only the needed part of the page is refreshed, so the page is **faster, uses less bandwidth and gives a smoother user experience**.
- Example: Google search suggestions, the Gmail inbox refresh, and "like" buttons.

**(b) Differentiate between Java and JavaScript.**

| Basis | Java | JavaScript |
|---|---|---|
| Type | Object-oriented **programming language** | Object-based **scripting language** |
| Execution | Compiled to bytecode and run on the **JVM** | **Interpreted / JIT** in the browser (or Node.js) |
| Typing | **Statically typed** (`int x`) | **Dynamically typed** (`let x`) |
| Developer | Sun Microsystems (James Gosling) | Netscape (Brendan Eich) |
| Used for | Desktop, Android, enterprise back end | Web front end, Node.js back end |
| Concurrency | Multi-threaded | Single-threaded event loop |
| File extension | `.java` / `.class` | `.js` |

**(c) Define a Datagram and its characteristics.**

- A **datagram** is an **independent, self-contained packet** of data sent over a network **without first setting up a connection**. It carries the full source and destination address. In Java it is used through the `DatagramPacket` and `DatagramSocket` classes (UDP).
- **Characteristics:**
  - **Connectionless:** no handshake is needed before sending.
  - **Unreliable:** delivery, order and duplicate removal are **not guaranteed**.
  - **Fast with low overhead:** no acknowledgements or retransmission.
  - **Fixed maximum size:** each packet is limited (about 64 KB for UDP).

---

### Q2. Explain the JavaScript Document Object Model (DOM). (7 Marks)

**1. Introduction / Definition**

The **Document Object Model (DOM)** is a **W3C standard, platform- and language-independent programming interface** that represents an HTML or XML document as a **tree of objects (nodes)**. JavaScript uses the DOM to **access, change, add or delete** elements, attributes, styles and content **dynamically**, without reloading the page.

**2. Block Diagram - DOM Tree**

```
   HTML source:
   <html>
     <head><title>My Page</title></head>
     <body>
       <h1 id="head">Hello</h1>
       <a href="x.html">Link</a>
     </body>
   </html>

                     +----------------+
                     |    document    |   (root object)
                     +-------+--------+
                             |
                     +-------v--------+
                     |    <html>      |   Element node
                     +---+--------+---+
                +--------+        +---------+
          +-----v-----+                +----v-----+
          |  <head>   |                |  <body>  |
          +-----+-----+                +--+----+--+
                |                   +-----+    +-----+
          +-----v-----+        +----v-----+   +------v------+
          |  <title>  |        |   <h1>   |   |    <a>      |
          +-----+-----+        | id="head"|   | href="x..." | <- Attribute node
                |              +----+-----+   +------+------+
          +-----v-----+        +----v-----+   +------v------+
          | "My Page" |        | "Hello"  |   |   "Link"    |  <- Text nodes
          +-----------+        +----------+   +-------------+
```

**3. Core Explanation / Working**

*(a) Types of DOM Nodes*

- **Document node:** the entire document (`document` object).
- **Element nodes:** HTML tags like `<body>` and `<p>`.
- **Attribute nodes:** attributes like `id` and `href`.
- **Text nodes:** the text inside elements.
- **Comment nodes:** `<!-- -->` comments.

*(b) Accessing (Selecting) Elements*

```javascript
document.getElementById("head");          // single element by id
document.getElementsByClassName("item");  // HTMLCollection
document.getElementsByTagName("p");       // HTMLCollection
document.querySelector(".item");          // first CSS-selector match
document.querySelectorAll("ul > li");     // NodeList of all matches
```

*(c) Modifying Content, Attributes and Styles*

```javascript
let h = document.getElementById("head");
h.innerHTML = "<i>Welcome</i>";           // change HTML content
h.textContent = "Welcome";                // change text only
h.setAttribute("class", "title");         // change attribute
h.style.color = "blue";                   // change CSS style
```

*(d) Creating and Deleting Nodes*

```javascript
let p = document.createElement("p");      // create element
p.textContent = "New paragraph";
document.body.appendChild(p);             // add to the tree
document.body.removeChild(p);             // remove from the tree
```

*(e) Traversing the Tree*

- `parentNode`, `childNodes`, `children`, `firstChild`, `lastChild`, `nextSibling`, `previousSibling`.

*(f) DOM Events (Event Handling)*

```javascript
let btn = document.getElementById("btn");
btn.addEventListener("click", function () {
    alert("Button clicked!");
});
```

- Common events: `click`, `submit`, `load`, `change`, `keyup`, `mouseover`.
- **Event propagation:** capturing (top-down), then target, then **bubbling** (bottom-up).

*(g) DOM Levels*

- **Level 0:** the original browser-specific model.
- **Level 1:** the core and HTML DOM.
- **Level 2:** events, styles, traversal.
- **Level 3:** keyboard events, XPath, load/save.

**4. Key Characteristics - `innerHTML` vs. `textContent`, HTML DOM vs. BOM**

| Basis | `innerHTML` | `textContent` |
|---|---|---|
| Reads / writes | HTML markup | Plain text only |
| Parses tags | Yes | No (tags shown as text) |
| Security | Risk of **XSS** with user input | Safe |
| Speed | Slower | Faster |

| Basis | DOM (Document Object Model) | BOM (Browser Object Model) |
|---|---|---|
| Represents | The **page content** | The **browser window** |
| Root object | `document` | `window` |
| Standard | W3C standard | No formal standard |
| Examples | `getElementById`, `createElement` | `alert()`, `location`, `history`, `navigator` |

**5. Advantages & Disadvantages**

*Advantages*

- Makes web pages **dynamic and interactive** without reloading.
- **Language and platform independent** (usable from JavaScript, Python, Java).
- It is the basis of **AJAX, SPAs and frameworks** (React uses a virtual DOM).

*Disadvantages*

- Frequent DOM changes cause **reflow and repaint**, which is **slow** for large documents.
- Careless use of `innerHTML` with user input leads to **XSS vulnerabilities**.

**6. Conclusion / Application**

The DOM powers every interactive web feature, such as **live form validation, image sliders, dropdown menus and dynamic content loading** on sites like YouTube and Gmail.

---

### Q3. Write a JavaScript program for client-side form validation (e.g., verifying a password field or empty inputs). (7 Marks)

**1. Introduction / Definition**

**Client-side form validation** means checking user input **in the browser, using JavaScript, before the form is sent** to the server. It gives users **instant feedback** and reduces needless server requests. Validation is attached to the form's **`onsubmit`** event, and returning `false` stops the submission.

**2. Flowchart - Validation Logic**

```
               +---------------------------+
               |  User clicks "Register"   |
               +-------------+-------------+
                             | onsubmit = validateForm()
               +-------------v-------------+
               |  Name field empty?        |--- Yes --> Show error, return false
               +-------------+-------------+
                             | No
               +-------------v-------------+
               |  Email format valid?      |--- No  --> Show error, return false
               |  (regex test)             |
               +-------------+-------------+
                             | Yes
               +-------------v-------------+
               |  Password >= 8 chars,     |--- No  --> Show error, return false
               |  has digit + uppercase +  |
               |  special character?       |
               +-------------+-------------+
                             | Yes
               +-------------v-------------+
               | Password == Confirm Pwd?  |--- No  --> Show error, return false
               +-------------+-------------+
                             | Yes
               +-------------v-------------+
               | Mobile = 10 digits?       |--- No  --> Show error, return false
               +-------------+-------------+
                             | Yes
               +-------------v-------------+
               |  return true              |
               |  -> Form sent to server   |
               +---------------------------+
```

**3. Core Explanation / Working - Program**

```html
<!DOCTYPE html>
<html>
<head>
  <title>Form Validation</title>
  <style>
    .error { color: red; font-size: 13px; }
  </style>
</head>
<body>
  <h2>Registration</h2>
  <form name="regForm" action="/register" method="post"
        onsubmit="return validateForm()">
    Name: <input type="text" id="name">
    <span class="error" id="nameErr"></span><br><br>

    Email: <input type="text" id="email">
    <span class="error" id="emailErr"></span><br><br>

    Password: <input type="password" id="pwd">
    <span class="error" id="pwdErr"></span><br><br>

    Confirm Password: <input type="password" id="cpwd">
    <span class="error" id="cpwdErr"></span><br><br>

    Mobile: <input type="text" id="mobile">
    <span class="error" id="mobErr"></span><br><br>

    <input type="submit" value="Register">
  </form>

  <script>
    function validateForm() {
      // Read and trim the values
      let name   = document.getElementById("name").value.trim();
      let email  = document.getElementById("email").value.trim();
      let pwd    = document.getElementById("pwd").value;
      let cpwd   = document.getElementById("cpwd").value;
      let mobile = document.getElementById("mobile").value.trim();
      let valid  = true;

      // Clear old error messages
      document.querySelectorAll(".error")
              .forEach(function (e) { e.textContent = ""; });

      // 1. Empty-field check
      if (name === "") {
        document.getElementById("nameErr").textContent = "Name is required";
        valid = false;
      }

      // 2. Email format check
      let emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
      if (!emailPattern.test(email)) {
        document.getElementById("emailErr").textContent = "Enter a valid email";
        valid = false;
      }

      // 3. Password strength check: min 8 chars, 1 uppercase,
      //    1 digit, 1 special character
      let pwdPattern = /^(?=.*[A-Z])(?=.*[0-9])(?=.*[!@#$%^&*]).{8,}$/;
      if (!pwdPattern.test(pwd)) {
        document.getElementById("pwdErr").textContent =
          "Min 8 chars with 1 uppercase, 1 digit and 1 special char";
        valid = false;
      }

      // 4. Confirm password check
      if (pwd !== cpwd) {
        document.getElementById("cpwdErr").textContent = "Passwords do not match";
        valid = false;
      }

      // 5. Mobile number check (exactly 10 digits)
      if (!/^[0-9]{10}$/.test(mobile)) {
        document.getElementById("mobErr").textContent = "Enter a 10-digit number";
        valid = false;
      }

      return valid;   // false stops the form submission
    }
  </script>
</body>
</html>
```

*Working*

- `onsubmit="return validateForm()"` runs the function **before** the form is sent.
- `.value.trim()` reads the input and removes extra spaces.
- `RegExp.test()` checks the format (email, password strength, mobile).
- Error messages appear in `<span>` elements through `textContent`, next to the wrong field.
- If any check fails, the function returns **`false`** and the submission is **cancelled**.

**4. Key Characteristics - Client-side vs. Server-side Validation**

| Basis | Client-side Validation | Server-side Validation |
|---|---|---|
| Runs on | Browser (JavaScript) | Web server (Servlet, Node.js) |
| Speed | **Instant** feedback | Needs a round trip |
| Security | **Can be bypassed** (JS can be disabled) | **Secure** and mandatory |
| Server load | Reduced | Increased |
| Purpose | User convenience | Data integrity and security |

**5. Advantages & Disadvantages**

*Advantages*

- **Immediate feedback** improves the user experience.
- **Reduces server load** and network traffic by catching errors early.
- Regular expressions allow **flexible format checks**.

*Disadvantages*

- It can be **bypassed** by disabling JavaScript or editing requests, so server checks are still needed.
- Validation logic is **visible** in the page source.

**6. Conclusion / Application**

Client-side validation is used on every **login, sign-up, payment and contact form**, for example checking the password strength on a Gmail or bank account registration page.

---

### Q4. Explain TCP/IP client sockets and write the constructor and methods used to create a client socket. (7 Marks)

**1. Introduction / Definition**

A **socket** is one **endpoint of a two-way communication link** between two programs on a network, identified by an **IP address and a port number**. A **TCP/IP client socket** (Java class **`java.net.Socket`**) connects to a server socket and gives a **reliable, connection-oriented, stream-based** link using TCP.

**2. Block Diagram - TCP Client-Server Socket Communication**

```
          CLIENT                                        SERVER
  +------------------------+                  +------------------------+
  |                        |                  | ServerSocket ss =      |
  |                        |                  |  new ServerSocket(5000)|
  |                        |                  +-----------+------------+
  |                        |                              |
  |                        |                  +-----------v------------+
  |                        |                  | Socket s = ss.accept() |
  |                        |                  |   (waits / blocks)     |
  +-----------+------------+                  +-----------+------------+
              |                                           ^
  +-----------v------------+   1. Connection request      |
  | Socket s = new Socket( |------ (3-way handshake) -----+
  |  "localhost", 5000)    |
  +-----------+------------+
              |
  +-----------v------------+   2. Request data            +------------------------+
  | s.getOutputStream()    |----------------------------->| s.getInputStream()     |
  |   write request        |                              |   read request         |
  +-----------+------------+                              +-----------+------------+
              |                                                       |
  +-----------v------------+   3. Response data           +-----------v------------+
  | s.getInputStream()     |<-----------------------------| s.getOutputStream()    |
  |   read response        |                              |   write response       |
  +-----------+------------+                              +-----------+------------+
              |                                                       |
  +-----------v------------+   4. Connection close        +-----------v------------+
  |      s.close()         |<---------------------------->|      s.close()         |
  +------------------------+                              +------------------------+
```

**3. Core Explanation / Working**

*(a) Steps to Create a TCP Client*

1. Create a `Socket` object with the server's **host name or IP** and **port**. This starts the TCP connection (three-way handshake).
2. Get the **input and output streams** from the socket.
3. **Send** a request through the output stream and **receive** the response through the input stream.
4. **Close** the streams and the socket.

*(b) Constructors of the `Socket` Class*

| Constructor | Description |
|---|---|
| `Socket(String host, int port)` | Connects to the given host name and port. Throws `UnknownHostException` or `IOException`. |
| `Socket(InetAddress address, int port)` | Connects using an `InetAddress` object and port. |
| `Socket(String host, int port, InetAddress localAddr, int localPort)` | Connects and also binds to a given **local** address and port. |
| `Socket(InetAddress addr, int port, InetAddress localAddr, int localPort)` | Same, using an InetAddress for the server. |
| `Socket()` | Creates an **unconnected** socket. Call `connect()` later. |

*(c) Important Methods of the `Socket` Class*

| Method | Purpose |
|---|---|
| `InputStream getInputStream()` | Returns the stream for **reading** data from the server |
| `OutputStream getOutputStream()` | Returns the stream for **writing** data to the server |
| `InetAddress getInetAddress()` | IP address of the **remote** host |
| `int getPort()` | Remote port number |
| `int getLocalPort()` | Local port the socket is bound to |
| `InetAddress getLocalAddress()` | Local IP address |
| `void connect(SocketAddress ep, int timeout)` | Connects an unconnected socket, with a timeout |
| `void setSoTimeout(int ms)` | Sets the read timeout |
| `boolean isConnected()` / `isClosed()` | Checks the connection state |
| `void close()` | Closes the socket and releases resources |

*(d) Program - TCP Client in Java*

```java
import java.io.*;
import java.net.*;

public class TCPClient {
    public static void main(String[] args) {
        try {
            // 1. Create the client socket (connects to the server)
            Socket s = new Socket("localhost", 5000);
            System.out.println("Connected to " + s.getInetAddress()
                               + " on port " + s.getPort());

            // 2. Get the I/O streams
            PrintWriter out = new PrintWriter(s.getOutputStream(), true);
            BufferedReader in = new BufferedReader(
                                new InputStreamReader(s.getInputStream()));

            // 3. Send a request and read the response
            out.println("Hello Server");
            String reply = in.readLine();
            System.out.println("Server says: " + reply);

            // 4. Close the resources
            in.close();
            out.close();
            s.close();
        } catch (UnknownHostException e) {
            System.out.println("Host not found: " + e.getMessage());
        } catch (IOException e) {
            System.out.println("I/O error: " + e.getMessage());
        }
    }
}
```

*Matching server, in short:* `ServerSocket ss = new ServerSocket(5000); Socket s = ss.accept();`, then read with `s.getInputStream()` and reply with `s.getOutputStream()`.

**4. Key Characteristics - TCP Socket vs. UDP Datagram Socket**

| Basis | TCP (`Socket`, `ServerSocket`) | UDP (`DatagramSocket`, `DatagramPacket`) |
|---|---|---|
| Connection | **Connection-oriented** | **Connectionless** |
| Reliability | Guaranteed delivery and order | Not guaranteed |
| Data unit | Continuous byte **stream** | Independent **packets** |
| Speed | Slower (handshake, ACKs) | Faster |
| Header size | 20 bytes | 8 bytes |
| Use case | HTTP, FTP, email, chat | Video streaming, DNS, online games |

**5. Advantages & Disadvantages**

*Advantages*

- **Reliable, ordered** delivery with error checking (TCP).
- The **stream-based API** makes reading and writing as easy as file I/O.
- **Platform independent** in Java.

*Disadvantages*

- **Connection set-up overhead** (three-way handshake) makes it slower than UDP.
- `accept()` and `read()` **block**, so threads are needed for many clients.

**6. Conclusion / Application**

TCP client sockets are the basis of **web browsers, chat applications, FTP clients and database drivers (JDBC)**, which all open a socket to talk to their servers.

---

## Unit 4: Java Beans & Enterprise Java Beans (EJB)

### Q1. Short Definitions (2 Marks Each)

**(a) What exactly is a Java Bean?**
- A **Java Bean** is a **reusable software component** written in Java that can be **visually manipulated in builder tools** (such as NetBeans). It follows the JavaBeans API conventions.
- **Rules (conventions) a class must follow:**
  1. It must have a **public no-argument constructor**.
  2. Its properties must be **private**, accessed through public **getter/setter** methods (`getName()`, `setName()`, and `isActive()` for booleans).
  3. It should implement **`java.io.Serializable`**, so its state can be saved and restored.

```java
public class Student implements java.io.Serializable {
    private String name;
    public Student() { }                          // no-arg constructor
    public String getName() { return name; }      // getter
    public void setName(String n) { name = n; }   // setter
}
```

**(b) What is the role of introspection in a Java Bean?**
- **Introspection** is the process by which a builder tool **automatically discovers a bean's properties, methods and events at run time**, without seeing its source code.
- It is done with the **`java.beans.Introspector`** class, which uses **Java Reflection** and the **naming conventions** (get/set/is), or an explicit **`BeanInfo`** class supplied by the developer.
- Role: it lets IDEs **show and edit bean properties visually** and **connect events**, which makes beans truly reusable "plug-and-play" components.
  `BeanInfo info = Introspector.getBeanInfo(Student.class);`

---

### Q2. Explain the complete EJB Architecture. (7 Marks)

**1. Introduction / Definition**

**Enterprise JavaBeans (EJB)** is a **server-side, component-based architecture** (part of Jakarta EE / Java EE) for building **distributed, transactional, secure and scalable** business applications. Business logic is written in **enterprise beans**, and these run inside an **EJB container**. The container automatically provides system-level services like transactions, security and persistence.

**2. Block Diagram - EJB Architecture**

```
  +-----------------+        +-------------------------------------------------+
  |    CLIENTS      |        |              EJB SERVER (App Server)            |
  |                 |        |      e.g. GlassFish, WildFly, WebLogic          |
  | +-------------+ |  RMI/  |  +-------------------------------------------+  |
  | | Web Client  | |  IIOP  |  |               EJB CONTAINER               |  |
  | |(Servlet/JSP)| +------->|  |                                           |  |
  | +-------------+ |  JNDI  |  |  +---------------+   +-----------------+  |  |
  | +-------------+ | lookup |  |  | Remote/Local  |-->|  Session Bean   |  |  |
  | | Java App    | +------->|  |  |  Interface    |   | (Business logic)|  |  |
  | | Client      | |        |  |  +---------------+   +-----------------+  |  |
  | +-------------+ |        |  |                      +-----------------+  |  |
  | +-------------+ |  JMS   |  |  JMS Queue/Topic --->| Message-Driven  |  |  |
  | | Messaging   | +------->|  |                      | Bean (MDB)      |  |  |
  | | Client      | |        |  |                      +-----------------+  |  |
  | +-------------+ |        |  |                      +-----------------+  |  |
  +-----------------+        |  |                      | Entity (JPA)    |  |  |
                             |  |                      +--------+--------+  |  |
                             |  |  Container Services:          |           |  |
                             |  |  Transactions (JTA) |Security |           |  |
                             |  |  Life cycle |Pooling|JNDI|    |           |  |
                             |  |  Concurrency | Persistence    |           |  |
                             |  +-------------------------------+-----------+  |
                             +----------------------------------+--------------+
                                                                |  JDBC
                                                       +--------v--------+
                                                       |    DATABASE     |
                                                       +-----------------+
```

**3. Core Explanation / Working**

*(a) Components of the EJB Architecture*
- **EJB Server:** the application server that provides the **run-time environment** and hosts one or more containers. Examples: GlassFish, JBoss/WildFly, WebLogic.
- **EJB Container:** a layer inside the server that **manages enterprise beans**. The client never talks to the bean directly. Every call goes **through the container**, which adds its services.
- **Enterprise Beans:** the components that hold the **business logic**.
  - **Session Beans:** do tasks for a client (stateless, stateful, singleton).
  - **Message-Driven Beans (MDB):** process **asynchronous JMS messages**.
  - **Entity Beans:** represent persistent data. In EJB 3.x they are replaced by **JPA entities**.
- **Interfaces:**
  - **Remote interface (`@Remote`):** for clients in **another JVM**, using RMI-IIOP.
  - **Local interface (`@Local`):** for clients in the **same JVM**, which is faster.
  - **Home interface** (EJB 2.x): a factory for creating and finding beans. It is no longer needed in EJB 3.x.
- **Deployment Descriptor (`ejb-jar.xml`) or annotations:** configure transactions, security and resources.
- **JNDI (Java Naming and Directory Interface):** clients **look up** beans by name.

*(b) Services Provided by the Container*
- **Transaction management (JTA):** automatic commit/rollback (`@TransactionAttribute`).
- **Security:** role-based access control (`@RolesAllowed`).
- **Life-cycle management and instance pooling:** creates, pools and destroys beans.
- **Concurrency control:** thread safety.
- **Persistence:** through JPA.
- **Remote access and location transparency.**

*(c) Working (request flow)*
1. The client **looks up** the bean through **JNDI**, or gets it through `@EJB` injection.
2. The container returns a **proxy (stub)** that implements the business interface.
3. The client calls a business method on the proxy.
4. The container **intercepts** the call, starts a transaction, checks security and gets a bean instance from the **pool**.
5. The bean runs the logic (and may use the database through JPA/JDBC).
6. The container **commits** the transaction and returns the result to the client.

*(d) Example (EJB 3.x)*

```java
@Stateless
public class BankBean implements BankRemote {
    public double getBalance(int accNo) { /* business logic */ return 5000.0; }
}

@Remote
public interface BankRemote { double getBalance(int accNo); }
```

**4. Key Characteristics - Types of Enterprise Beans**

| Basis | Session Bean | Message-Driven Bean | Entity (JPA) |
|---|---|---|---|
| Purpose | Business logic / tasks | Asynchronous message processing | Persistent data |
| Invocation | Synchronous (method call) | Asynchronous (JMS message) | Through EntityManager |
| Client state | Stateful or stateless | Stateless | Represents a DB row |
| Annotation | `@Stateless`, `@Stateful`, `@Singleton` | `@MessageDriven` | `@Entity` |
| Survives server crash | No | No | **Yes** (stored in DB) |

**5. Advantages & Disadvantages**

*Advantages*
- The developer writes **only business logic**. The container handles transactions, security and pooling.
- **Scalable and distributed**: beans can be accessed remotely and clustered.
- **Portable** across any Java EE-compliant application server.

*Disadvantages*
- Needs a **heavyweight application server**, which uses more resources.
- **Complex** compared with lightweight frameworks like Spring Boot, with a steeper learning curve.
- Remote calls add **network overhead**.

**6. Conclusion / Application**

EJB is used in **banking, insurance, airline reservation and large enterprise ERP systems**, which need distributed transactions and high security.

---

### Q3. Differentiate between a Java Bean and an Enterprise Java Bean (EJB). (7 Marks)

**1. Introduction / Definition**

A **Java Bean** is a simple, **client-side or general-purpose reusable component** that follows naming conventions and is used mainly in builder tools and for data transfer. An **Enterprise Java Bean (EJB)** is a **server-side, distributed business component** that runs inside an **EJB container**, which provides transaction, security and life-cycle services.

**2. Block Diagram - Where Each Runs**

```
   JAVA BEAN                                ENTERPRISE JAVA BEAN
   +------------------------------+         +----------------------------------+
   |  Any JVM (Desktop / Web app) |         |   Application Server (JVM)       |
   |  +------------------------+  |         |  +----------------------------+  |
   |  |  Student Bean          |  |         |  |       EJB CONTAINER        |  |
   |  |  - private fields      |  |         |  |  +----------------------+  |  |
   |  |  - get/set methods     |  |         |  |  | BankBean (@Stateless)|  |  |
   |  |  - no-arg constructor  |  |         |  |  +----------------------+  |  |
   |  |  - Serializable        |  |         |  |  Transactions | Security   |  |
   |  +------------------------+  |         |  |  Pooling | JNDI | Remote   |  |
   |   Used directly with `new`   |         |  +----------------------------+  |
   +------------------------------+         +---------------^------------------+
                                                            | RMI-IIOP / JNDI
                                                    +-------+--------+
                                                    | Remote Clients |
                                                    +----------------+
```

**3. Core Explanation / Working**

*Java Bean*
- A **plain Java class** that follows conventions: a no-arg constructor, private properties with getters/setters, and `Serializable`.
- Created directly with `new`, or with `<jsp:useBean>` in JSP.
- Used for **GUI components (Swing/AWT)**, **data holders (DTOs)** and **JSP form beans**.
- Supports **properties, events, introspection, customization and persistence**.

*Enterprise Java Bean*
- A **managed component**. It is **never created with `new`** by the client. The **container** creates, pools and destroys it.
- It is accessed through **business interfaces** (local or remote) using **JNDI lookup** or `@EJB` injection.
- Types: **Session beans** (stateless, stateful, singleton) and **Message-Driven beans**.
- Gets **declarative services**: transactions, security, concurrency and remoting.

**4. Key Characteristics - Comparison Table**

| Basis | Java Bean | Enterprise Java Bean (EJB) |
|---|---|---|
| Nature | Simple reusable component | Distributed **server-side** business component |
| Runs in | Any JVM (no container needed) | Only inside an **EJB container** (application server) |
| Created by | Programmer (`new`) or builder tool | **Container** |
| API / package | `java.beans` | `javax.ejb` / `jakarta.ejb` |
| Interfaces needed | None | Business interface (`@Local` / `@Remote`) |
| Remote access | Not supported | Supported (RMI-IIOP) |
| Transactions and security | Must be coded manually | **Provided by the container** (declarative) |
| Persistence | Through serialization | Through JPA / database |
| Visual (GUI) use | Yes (builder tools) | No visual representation |
| Examples | Swing button, Student DTO | Banking service bean, order-processing bean |
| Complexity | Low | High |

**5. Advantages & Disadvantages**

*Java Bean*
- *Advantages:* **simple and lightweight**; reusable in any Java application; easy to use in JSP and IDEs.
- *Disadvantages:* **no built-in enterprise services** (transactions, security); cannot be called remotely.

*EJB*
- *Advantages:* **container-managed services**; supports **distributed and scalable** applications.
- *Disadvantages:* needs a **heavy application server**; **more complex** to develop and deploy.

**6. Conclusion / Application**

Java Beans are used as **data and UI components in desktop and JSP applications**, while EJBs implement **core business services in enterprise banking and e-commerce back ends**.

---

### Q4. Explain session beans and detail their various types (Stateful vs. Stateless). (7 Marks)

**1. Introduction / Definition**

A **session bean** is an enterprise bean that **performs business tasks for a client** during a session, such as calculations, bank transfers or order processing. It is **not persistent**: it does not represent data in the database and it is lost when the server shuts down. There are three types: **Stateless, Stateful and Singleton**.

**2. Block Diagram - Session Bean Types**

```
   STATELESS (@Stateless)              STATEFUL (@Stateful)             SINGLETON (@Singleton)
   +-----------------------+           +----------------------+         +----------------------+
   |   Instance POOL       |           | Client A -> Bean A   |         | Client A --+         |
   | +----+ +----+ +----+  |           |   (cart: 3 items)    |         | Client B --+--> ONE  |
   | | B1 | | B2 | | B3 |  |           | Client B -> Bean B   |         | Client C --+   Bean  |
   | +----+ +----+ +----+  |           |   (cart: 1 item)     |         |  (shared state,      |
   |   ^      ^      ^     |           |                      |         |   one per app)       |
   +---+------+------+-----+           | One bean per client, |         +----------------------+
       |      |      |                 | keeps conversational |
    Any client gets any free           | state across calls   |
    instance; no state kept            +----------------------+
    between calls
```

*Life cycle of a Stateful Session Bean*

```
                     @PostConstruct
 +----------------+ -----------------> +---------+   @PrePassivate    +-----------+
 | Does Not Exist |                    |  READY  | -----------------> |  PASSIVE  |
 +----------------+ <----------------- +---------+ <----------------- | (on disk) |
                  @Remove / @PreDestroy                @PostActivate  +-----------+

 Stateless bean: only "Does Not Exist" <-> "Ready (pooled)"; there is no Passive state.
```

**3. Core Explanation / Working**

*(a) Stateless Session Bean (`@Stateless`)*
- Keeps **no conversational state** for the client between method calls.
- Any free instance from the **pool** can serve any client, so instances are **shared**.
- **Highly scalable**, because a few instances serve thousands of clients.
- Life cycle: Does Not Exist, then Method-Ready Pool. Callbacks: `@PostConstruct`, `@PreDestroy`.
- Example: currency converter, tax calculator, sending email.

```java
@Stateless
public class CalculatorBean {
    public int add(int a, int b) { return a + b; }
}
```

*(b) Stateful Session Bean (`@Stateful`)*
- Keeps **conversational state** for **one specific client** across many method calls.
- There is **one instance per client**, and the instances are not shared.
- If the bean is idle, the container can **passivate** it (save its state to disk) and **activate** it later.
- It ends when the client calls a method marked `@Remove`, or after a timeout.
- Callbacks: `@PostConstruct`, `@PrePassivate`, `@PostActivate`, `@PreDestroy`.
- Example: **shopping cart**, online exam session, multi-step booking.

```java
@Stateful
public class CartBean {
    private List<String> items = new ArrayList<>();
    public void addItem(String item) { items.add(item); }
    public List<String> getItems() { return items; }
    @Remove
    public void checkout() { /* place order, bean is removed */ }
}
```

*(c) Singleton Session Bean (`@Singleton`)* (EJB 3.1)
- **Only one instance per application**, shared by all clients.
- Used for **shared application state**: cache, configuration, counters.
- Concurrency is controlled with `@Lock(READ)` and `@Lock(WRITE)`. With `@Startup` it is created when the application starts.

**4. Key Characteristics - Stateful vs. Stateless**

| Basis | Stateless Session Bean | Stateful Session Bean |
|---|---|---|
| Conversational state | **Not kept** between calls | **Kept** for one client |
| Instance-to-client | Shared from a pool | **One instance per client** |
| Scalability | **Very high** | Lower (more memory) |
| Passivation / activation | Not needed | Supported |
| Life-cycle states | Does Not Exist, Ready | Does Not Exist, Ready, **Passive** |
| Annotation | `@Stateless` | `@Stateful` (+ `@Remove`) |
| Performance | Faster | Slower |
| Example | Tax calculator, email sender | Shopping cart, booking wizard |

**5. Advantages & Disadvantages**

*Advantages*
- Business logic is **separated** from the presentation layer.
- The container provides **transactions, security and pooling** automatically.
- **Stateless beans scale** very well. **Stateful beans make multi-step workflows simple**.

*Disadvantages*
- Stateful beans use **more memory** and passivation adds **I/O overhead**.
- Session beans are **not persistent**, so their data is lost on a crash unless it is saved to a database.

**6. Conclusion / Application**

Stateless beans implement **payment and calculation services**, while stateful beans implement **shopping carts on e-commerce sites and step-by-step ticket booking** in reservation systems.

---

## Unit 5: Modern Backend (Servlets, JSP, Node.js & MongoDB)

### Q1. Short Definitions (2 Marks Each)

**(a) What is Node.js and what is its primary use case?**
- **Node.js** is an **open-source, cross-platform JavaScript run-time environment** built on Google Chrome's **V8 engine**. It lets JavaScript run **on the server**, outside the browser. It uses a **single-threaded, event-driven, non-blocking I/O** model.
- **Primary use case:** building **fast, scalable network applications that handle many requests at once and spend most of their time on I/O**, such as **REST APIs, real-time chat apps (Socket.io), streaming services and microservices**.

**(b) What is the purpose of the `HttpServletRequest` interface?**
- `javax.servlet.http.HttpServletRequest` (it extends `ServletRequest`) **represents the client's HTTP request**. The servlet container creates it and passes it to the servlet's `service()` / `doGet()` / `doPost()` methods.
- **Purpose:** it lets the servlet **read everything the client sent**:
  - Form parameters: `getParameter("name")`, `getParameterValues()`
  - Headers: `getHeader("User-Agent")`
  - Cookies and session: `getCookies()`, `getSession()`
  - Request information: `getMethod()`, `getRequestURI()`, `getRemoteAddr()`
  - Request attributes for forwarding: `setAttribute()`, `getAttribute()`

---

### Q2. Discuss the compilation process of JSP files into Servlets and how they are executed by the container. (7 Marks)

**1. Introduction / Definition**

**JSP (JavaServer Pages)** is a server-side technology for creating dynamic web pages by **embedding Java code in HTML**. A JSP page is **not run directly**. The **JSP container (for example Tomcat's Jasper engine)** first **translates it into a Java Servlet**, **compiles** that servlet into bytecode, and then **runs** it like any other servlet.

**2. Block Diagram - JSP Processing / Life Cycle**

```
  +-----------+  1. HTTP Request (hello.jsp)   +--------------------------------------+
  |  Browser  |------------------------------->|        WEB SERVER / CONTAINER        |
  |  (Client) |                                |             (Tomcat)                 |
  +-----^-----+                                |                                      |
        |                                      |   +------------------------------+   |
        |                                      |   | First request or JSP changed?|   |
        |                                      |   +-------+--------------+-------+   |
        |                                      |       Yes |              | No        |
        |                                      |   +-------v-------+      |           |
        |                                      |   | 2. TRANSLATION|      |           |
        |                                      |   | hello.jsp ->  |      |           |
        |                                      |   | hello_jsp.java|      |           |
        |                                      |   +-------+-------+      |           |
        |                                      |   +-------v-------+      |           |
        |                                      |   | 3. COMPILATION|      |           |
        |                                      |   | -> hello_jsp  |      |           |
        |                                      |   |    .class     |      |           |
        |                                      |   +-------+-------+      |           |
        |                                      |   +-------v-------+      |           |
        |                                      |   | 4. LOADING &  |      |           |
        |                                      |   | INSTANTIATION |      |           |
        |                                      |   +-------+-------+      |           |
        |                                      |   +-------v-------+      |           |
        |                                      |   | 5. jspInit()  |      |           |
        |                                      |   +-------+-------+      |           |
        |                                      |   +-------v--------------v-------+   |
        |     7. HTTP Response (HTML)          |   | 6. _jspService(req, res)     |   |
        +--------------------------------------+---|  (runs on EVERY request)     |   |
                                               |   +------------------------------+   |
                                               |   | 8. jspDestroy() (on undeploy)|   |
                                               |   +------------------------------+   |
                                               +--------------------------------------+
```

**3. Core Explanation / Working**

*Phase 1 - Translation*
- On the **first request** (or after the JSP file changes), the JSP engine **parses** `hello.jsp` and creates the Java source file `hello_jsp.java`.
- The generated class extends `HttpJspBase`, which implements the `HttpJspPage` interface.
- Mapping of JSP elements to servlet code:
  - Static HTML becomes `out.write("...")` statements.
  - Scriptlet `<% code %>` is copied into `_jspService()`.
  - Expression `<%= expr %>` becomes `out.print(expr)`.
  - Declaration `<%! int x; %>` becomes a class-level field or method.
  - Directive `<%@ page import="java.util.*" %>` becomes `import` statements and settings.

*Phase 2 - Compilation*
- The container compiles `hello_jsp.java` with the Java compiler into **`hello_jsp.class`** (bytecode).
- Syntax errors in the JSP appear at this stage as compilation errors.

*Phase 3 - Class Loading and Instantiation*
- The class loader **loads** `hello_jsp.class`, and the container creates **one instance** of it.

*Phase 4 - Initialization: `jspInit()`*
- Called **once**, to set up resources like database connections. It can be overridden in a declaration.

*Phase 5 - Request Processing: `_jspService(request, response)`*
- Called for **every request**, each in a **separate thread**. It produces the dynamic HTML response.
- **Implicit objects** are available here: `request`, `response`, `out`, `session`, `application`, `config`, `pageContext`, `page`, `exception`.
- It **cannot be overridden** (the underscore marks it as container-generated).

*Phase 6 - Destruction: `jspDestroy()`*
- Called **once** when the JSP is removed or the server shuts down, to release resources.

*Example*

```jsp
<%@ page contentType="text/html" %>
<html><body>
  <% String user = request.getParameter("name"); %>
  <h2>Welcome, <%= user %>!</h2>
</body></html>
```

*The generated servlet (simplified):*

```java
public final class hello_jsp extends HttpJspBase {
  public void _jspService(HttpServletRequest request, HttpServletResponse response)
        throws IOException, ServletException {
    JspWriter out = pageContext.getOut();
    out.write("<html><body>\n");
    String user = request.getParameter("name");
    out.write("<h2>Welcome, ");
    out.print(user);
    out.write("!</h2>\n</body></html>");
  }
}
```

- **Later requests skip translation and compilation.** The already-loaded instance runs `_jspService()` directly, so only the first request is slow.

**4. Key Characteristics - JSP vs. Servlet**

| Basis | JSP | Servlet |
|---|---|---|
| Code style | Java inside HTML | HTML inside Java (`out.println`) |
| Best for | **Presentation (View)** | **Business logic (Controller)** |
| Translation step | Yes (JSP to Servlet) | No |
| First request | Slower (translate + compile) | Faster |
| Recompile on change | **Automatic** | Manual recompile and redeploy |
| Implicit objects | Available (`request`, `out`, `session`) | Must be obtained manually |
| Life-cycle methods | `jspInit`, `_jspService`, `jspDestroy` | `init`, `service`, `destroy` |

**5. Advantages & Disadvantages**

*Advantages*
- **Easier to write and maintain** than servlets for HTML-heavy pages.
- **Automatic recompilation** when the JSP changes.
- Supports **tag libraries (JSTL)** and Expression Language, which reduce Java code in pages.

*Disadvantages*
- The **first request is slow**, because of translation and compilation.
- Mixing Java and HTML makes pages **hard to debug and maintain** if scriptlets are overused.

**6. Conclusion / Application**

JSP is used as the **View layer in MVC web applications** (with servlets as controllers), for example in **online banking portals and college result systems** running on Apache Tomcat.

---

### Q3. Explain the Servlet lifecycle methods (`init`, `service`, `destroy`). (7 Marks)

**1. Introduction / Definition**

A **Servlet** is a server-side Java class that **handles HTTP requests and generates dynamic responses** inside a **servlet container** (for example Apache Tomcat). The **servlet life cycle** is the sequence of stages from the servlet's **creation to its destruction**. The container controls it through the three methods of the `javax.servlet.Servlet` interface: **`init()`, `service()` and `destroy()`**.

**2. Block Diagram - Servlet Life Cycle**

```
                   +-------------------------------------+
                   |  1. LOADING the servlet class       |   (first request or
                   |     (Class.forName by container)    |    load-on-startup)
                   +------------------+------------------+
                                      |
                   +------------------v------------------+
                   |  2. INSTANTIATION                   |   Only ONE object
                   |     (no-arg constructor called)     |
                   +------------------+------------------+
                                      |
                   +------------------v------------------+
                   |  3. init(ServletConfig config)      |   Called ONCE
                   |     - read config, open DB conn     |
                   +------------------+------------------+
                                      |
                                      v
                   +-------------------------------------+
     Request 1 --->|  4. service(ServletRequest,         |   Called for EVERY
     Request 2 --->|            ServletResponse)         |   request, each in
     Request n --->|     -> doGet() / doPost() /         |   a NEW THREAD
                   |        doPut() / doDelete()         |
                   +------------------+------------------+
                                      |  (server shutdown /
                                      |   undeploy / reload)
                   +------------------v------------------+
                   |  5. destroy()                       |   Called ONCE
                   |     - close DB conn, release memory |
                   +------------------+------------------+
                                      |
                   +------------------v------------------+
                   |  6. Garbage Collection              |
                   +-------------------------------------+
```

**3. Core Explanation / Working**

*Step 1 & 2 - Loading and Instantiation*
- The container **loads** the servlet class when the **first request** arrives, or at **server start-up** if `<load-on-startup>` is set in `web.xml`.
- It creates **exactly one instance** using the public no-arg constructor.

*Step 3 - `init()` Method*
- Signature: `public void init(ServletConfig config) throws ServletException`
- Called **only once**, right after instantiation and **before any request** is handled.
- Used for **one-time set-up**: reading init parameters, opening database connections, loading configuration.
- If it throws `ServletException`, the servlet is not put into service.

*Step 4 - `service()` Method*
- Signature: `public void service(ServletRequest req, ServletResponse res) throws ServletException, IOException`
- Called **for every client request**. The container creates a **new thread** for each request, all on the **same instance**, so shared fields must be thread-safe.
- In `HttpServlet`, `service()` checks the HTTP method and **dispatches** to `doGet()`, `doPost()`, `doPut()`, `doDelete()` and so on.
- Developers usually override `doGet()` and `doPost()`, not `service()`.

*Step 5 - `destroy()` Method*
- Signature: `public void destroy()`
- Called **only once**, when the servlet is taken out of service (server shutdown, application undeploy or reload).
- Used to **release resources**: close connections, stop threads, save state.
- After this, the instance is **garbage-collected**.

*Example Program*

```java
import java.io.*;
import javax.servlet.*;
import javax.servlet.http.*;

public class LifeCycleServlet extends HttpServlet {

    public void init(ServletConfig config) throws ServletException {
        super.init(config);
        System.out.println("init(): servlet initialized (called once)");
    }

    protected void doGet(HttpServletRequest req, HttpServletResponse res)
            throws ServletException, IOException {
        res.setContentType("text/html");
        PrintWriter out = res.getWriter();
        String name = req.getParameter("name");
        out.println("<h2>Hello, " + name + "</h2>");   // runs per request
    }

    public void destroy() {
        System.out.println("destroy(): servlet destroyed (called once)");
    }
}
```

*Deployment descriptor (`web.xml`)*

```xml
<servlet>
  <servlet-name>life</servlet-name>
  <servlet-class>LifeCycleServlet</servlet-class>
  <load-on-startup>1</load-on-startup>
</servlet>
<servlet-mapping>
  <servlet-name>life</servlet-name>
  <url-pattern>/hello</url-pattern>
</servlet-mapping>
```

(Alternatively, use the annotation `@WebServlet("/hello")` in Servlet 3.0+.)

**4. Key Characteristics - Life-Cycle Methods**

| Basis | `init()` | `service()` | `destroy()` |
|---|---|---|---|
| Called by | Container | Container | Container |
| How many times | **Once** | **Once per request** | **Once** |
| When | After instantiation | On each client request | Before removal |
| Parameters | `ServletConfig` | `ServletRequest`, `ServletResponse` | None |
| Purpose | Initialize resources | Process the request, build the response | Release resources |
| Threading | Single thread | **Multi-threaded** | Single thread |

**5. Advantages & Disadvantages** (of the servlet life-cycle model)

*Advantages*
- **One instance, many threads**: much faster and lighter than CGI, which starts a new process per request.
- **One-time initialization** in `init()` avoids repeated costly set-up.
- **Clean resource release** in `destroy()` prevents memory leaks.

*Disadvantages*
- Instance variables are shared by all threads, so **thread-safety problems** (race conditions) must be handled.
- The **first request is slower** (loading and `init()`) unless `load-on-startup` is used.

**6. Conclusion / Application**

The servlet life cycle is the basis of **every Java web framework (Spring MVC's DispatcherServlet, Struts)** and of login handlers, form processors and REST endpoints on Apache Tomcat.

---

### Q4. Outline the step-by-step process to set up Node.js in Windows and create a MongoDB database connection. (7 Marks)

**1. Introduction / Definition**

**Node.js** is a JavaScript run time for building server-side applications, and **MongoDB** is a **NoSQL, document-oriented database** that stores data as **JSON-like BSON documents** in **collections**. Node.js connects to MongoDB using the official **`mongodb` driver** or the **Mongoose ODM** library.

**2. Block Diagram - Set-up and Connection Flow**

```
  +-------------------------------+      +-------------------------------+
  | 1. Download Node.js LTS (.msi)|      | 5. Install MongoDB Community  |
  |    from nodejs.org            |      |    Server (.msi) + Compass    |
  +---------------+---------------+      |    (or use MongoDB Atlas)     |
                  |                      +---------------+---------------+
  +---------------v---------------+                      |
  | 2. Run installer (adds node + |      +---------------v---------------+
  |    npm to PATH)               |      | 6. Start the service: mongod  |
  +---------------+---------------+      |    on localhost:27017         |
                  |                      +---------------+---------------+
  +---------------v---------------+                      |
  | 3. Verify: node -v , npm -v   |                      |
  +---------------+---------------+                      |
                  |                                      |
  +---------------v---------------+                      |
  | 4. mkdir project; npm init -y;|                      |
  |    npm install mongodb        |                      |
  +---------------+---------------+                      |
                  |                                      |
  +---------------v--------------------------------------v---------------+
  | 7. app.js:  MongoClient.connect("mongodb://localhost:27017")         |
  +----------------------------------+-----------------------------------+
                                     |
  +----------------------------------v-----------------------------------+
  |   NODE.JS APP  <------ MongoDB Driver (TCP) ------>  MONGODB SERVER   |
  |   (app.js)                                          DB -> Collection |
  |                                                        -> Documents  |
  +----------------------------------------------------------------------+
```

**3. Core Explanation / Working**

*Part A - Installing Node.js on Windows*
1. Open **https://nodejs.org** and download the **LTS (Long Term Support)** Windows Installer (`.msi`, 64-bit).
2. Run the installer and accept the licence. Keep the default path `C:\Program Files\nodejs\`. Make sure **"Add to PATH"** and the **npm package manager** are selected. Click **Install**.
3. Open **Command Prompt** and check the installation:

```bash
node -v      # e.g. v20.x.x
npm -v       # e.g. 10.x.x
```

4. Create a project folder and initialise it:

```bash
mkdir myapp
cd myapp
npm init -y               # creates package.json
npm install mongodb       # official MongoDB driver
```

*Part B - Installing and Starting MongoDB*

5. Download **MongoDB Community Server** (`.msi`) from **mongodb.com**. Choose **"Complete"** set-up and **"Install MongoDB as a Service"**. Optionally install **MongoDB Compass** (GUI).
6. The MongoDB service starts automatically and listens on **`localhost:27017`**. Check it with `mongosh` in the terminal.
   - *Alternative:* create a free cloud cluster on **MongoDB Atlas** and copy its connection string (`mongodb+srv://...`).

*Part C - Creating the Database Connection (`app.js`)*

```javascript
// app.js
const { MongoClient } = require("mongodb");

const url = "mongodb://127.0.0.1:27017";   // connection string
const client = new MongoClient(url);
const dbName = "collegeDB";

async function main() {
    try {
        // 1. Connect to the MongoDB server
        await client.connect();
        console.log("Connected successfully to MongoDB");

        // 2. Select the database (created automatically on first insert)
        const db = client.db(dbName);
        const students = db.collection("students");

        // 3. Insert a document
        const result = await students.insertOne(
            { roll: 101, name: "Harsh", branch: "CSE", year: 3 });
        console.log("Inserted id:", result.insertedId);

        // 4. Read documents
        const data = await students.find({ branch: "CSE" }).toArray();
        console.log(data);
    } catch (err) {
        console.error("Connection error:", err);
    } finally {
        // 5. Close the connection
        await client.close();
    }
}

main();
```

7. Run the program:

```bash
node app.js
```

*Output:*

```
Connected successfully to MongoDB
Inserted id: 6650f1c2a4...
[ { _id: ..., roll: 101, name: 'Harsh', branch: 'CSE', year: 3 } ]
```

*Alternative using Mongoose (schema-based ODM)*

```javascript
const mongoose = require("mongoose");          // npm install mongoose
mongoose.connect("mongodb://127.0.0.1:27017/collegeDB")
        .then(() => console.log("Mongoose connected"))
        .catch(err => console.log(err));
const Student = mongoose.model("Student",
        new mongoose.Schema({ roll: Number, name: String }));
```

**4. Key Characteristics - MongoDB (NoSQL) vs. MySQL (SQL)**

| Basis | MongoDB | MySQL |
|---|---|---|
| Data model | **Documents** (JSON/BSON) | **Tables** (rows and columns) |
| Schema | **Flexible / schema-less** | Fixed schema |
| Query language | JavaScript-like methods (`find`, `insertOne`) | SQL |
| Scaling | **Horizontal** (sharding) | Mainly vertical |
| Joins | Limited (`$lookup`) | Full support |
| Best with | Node.js (MERN / MEAN stack) | PHP, Java (LAMP) |

**5. Advantages & Disadvantages**

*Advantages*
- **JavaScript end to end**: Node.js and MongoDB both use JSON, so no data conversion is needed.
- **Non-blocking async I/O** handles many concurrent database requests efficiently.
- **Flexible schema** speeds up development, and data scales horizontally.

*Disadvantages*
- No full **ACID joins** like SQL. Complex relational queries are harder.
- Node.js is **not suited to CPU-heavy tasks**, which block its single thread.
- The flexible schema can lead to **inconsistent data** without validation (Mongoose helps).

**6. Conclusion / Application**

Node.js with MongoDB forms the back end of the **MERN/MEAN stack**, used in **real-time chat apps, e-commerce sites and social media platforms** (for example parts of Netflix, Uber and LinkedIn).

---

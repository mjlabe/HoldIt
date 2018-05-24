#Templates

The templates are divided up by groups so that:
* Each group has its own **privileges** as well as the **privileges** of the group below
* Only users in the corresponding group can view that group's pages (and the pages with lower privilege)
* The **hierarchy privilege** is in the following order (highest privilege to lowest), with details below:
    1) Admin
    2) Worker
    3) Contributor
    4) User
    5) Public


##Base Templates

These templates include the basic formatting, CSS, and javascript in which all other templates inherit (extend) from.

These pages are visible to **anyone**, regardless of what group they belong to. Be sure to limit the pages in this view
since it is a **security risk**.

The following templates belong to **base**:

* [base](base/base.html)
* [header](base/header.html)
* [footer](base/footer.html)


##Registration Templates

These templates allow a user to login, signup, and logout.

These pages are visible to **anyone**, regardless of what group they belong to. Be sure to limit the pages in this view
since it is a **security risk**.

The following templates belong to **registration**:

* [login](registration/login.html)
* logout (this is a built-in Django url with no 'real' template)
* [signup](registration/signup.html)
* [success](registration/signup_success.html)


##Public Templates

These templates include pages we want anyone to be able to see whether they are logged in or not. This can include the 
home, contact, and info pages, for example.

These pages are visible to **anyone**, regardless of what group they belong to. Be sure to limit the pages in this view
since it is a **security risk**.

The following views belong to **public**:

* [index](public/index.html)

Since these pages are **public**, be sure to limit what information is on the page. Also, think carefully
about adding more views to **public**; we want to limit access to the content and keep it **secure**.


##User Templates

These pages are limited to users that only have **read privileges**. We are limiting this view 

The following templates belong to **user**:

* [report_detail](user/report_detail.html)
* [report_list](user/report_list.html)

##Contributor Views

These pages are limited to users that have **read privileges** and **limited write privileges**.

The following templates belong to **contributor**:

* [new_report](contributor/new_report.html)


##Worker Templates

These pages are limited to users that have **read privileges** and **limited write privileges**.

The following templates belong to **worker**:

*


##Admin Templates

User with **admin** privileges can view any page and have their own pages for administrative tasks.

The following templates belong to **admin**:

*

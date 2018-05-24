#Views

The views are divided up by groups so that:
* Only logged in users can view restricted pages
* Each group has its own **privileges** as well as the **privileges** of the group below
* Only users in the corresponding group can view that group's views/pages (and the views/pages with lower privilege)
* The **hierarchy privilege** is in the following order (highest privilege to lowest), with details below:
    1) Admin
    2) Worker
    3) Contributor
    4) User
    5) Public
    
The **decorator** is placed at the top of every view to limit access to that view. 

A better implementation would include custom **Middleware** to limit access to **all** pages by default. That way, if
a view or page didn't have the the above (or corresponding **decorator**), the page/view would not be accessible. 



##Public Views

These views are visible to **anyone**, regardless of what group they belong to. Be sure to limit the pages in this view
since it is a **security risk**.

The following views belong to [views_public](../views/views_public.py):

* login
* logout
* signup
* success
* index

Since **index** (our homepage) is **public**, be sure to limit what information is on the page. Also, think carefully
about adding more views to **views_public**; we want to limit access to the content and keep it **secure**.


##User Views

These views are limited to users that only have **read privileges**.

Right now, the following code is used to limit access to [views_user](../views/views_user.py):

<pre><code>def is_user(user):
    return user.groups.filter(name='User').exists()
 
@user_passes_test(is_user)          #decorator for the beginning of each view
</code></pre>

The following views belong to **views_user**:

* report_detail
* report_list

##Contributor Views

These views are limited to users that have **read privileges** and **limited write privileges**.

Right now, the following code is used to limit access to to [views_contrib](../views/views_contrib.py):

<pre><code>def is_contributor(user):
    return user.groups.filter(name='Contributor').exists()
 
@user_passes_test(is_contributor)   #decorator for the beginning of each view
</code></pre>

The following views belong to **views_contrib**:

* new_report


##Worker Views

These views are limited to users that have **read privileges** and **limited write privileges**.

Right now, the following code is used to limit access to to [views_worker](../views/views_worker.py):

<pre><code>def is_worker(user):
    return user.groups.filter(name='Worker').exists()
 
@user_passes_test(is_worker)   #decorator for the beginning of each view
</code></pre>

The following views belong to **views_worker**:

*


##Admin Views

User with **admin** privileges can view any page/view and have their own pages for administrative tasks.

Right now, the following code is used to limit access to to [views_admin](../views/views_admin.py):

<pre><code>def is_admin(user):
    return user.groups.filter(name='Admin').exists()
 
@user_passes_test(is_Admin)   #decorator for the beginning of each view
</code></pre>

The following views belong to **views_admin**:

*

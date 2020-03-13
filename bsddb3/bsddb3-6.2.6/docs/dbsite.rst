==========
DBSite
==========

Read :Oracle:`Oracle documentation <programmer_reference/group_membership.html>`
for better understanding.

You use the DB_SITE handle to configure and manage replication sites.

:OracleAPIC:`More info... <repmgr_site.html>`

DBSite Methods
------------------

.. function:: close(flags=0)

   Close a DBSite handle.
   :OracleAPIC:`More info... <dbsite_close.html>`

.. function:: get_address()

   Returns a replication site's network address. That is, this method
   returns a tuple with the site's hostname and port. 
   :OracleAPIC:`More info... <dbsite_get_address.html>`

.. function:: get_config()

   Returns whether the specified which parameter is currently set.
   :OracleAPIC:`More info... <dbsite_get_config.html>`

.. function:: get_eid()

   Returns a replication site's Environment ID (EID).
   :OracleAPIC:`More info... <dbsite_get_eid.html>`

.. function:: remove()

   Removes the site from the replication group. If called at the master
   site, repmgr updates the membership database directly. If called from
   a client, this method causes a request to be sent to the master to
   perform the operation. The method then awaits confirmation.
   :OracleAPIC:`More info... <dbsite_remove.html>`

.. function:: set_config(which, value)

   Configures a replication site.
   :OracleAPIC:`More info... <dbsite_set_config.html>`



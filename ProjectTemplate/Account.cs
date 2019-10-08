using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;

namespace ProjectTemplate
{
    public class Account
    {
        //this is just a container for all info related
        //to an account.  We'll simply create public class-level
        //variables representing each piece of information!
        public string userId;
        public string password;
        public string firstName;
        public string lastName;
        public string email;
        public string username;

        public Account(string userId, string password, string firstName, string lastName, string email, string username)
        {
            this.userId = userId;
            this.password = password;
            this.firstName = firstName;
            this.lastName = lastName;
            this.email = email;
            this.username = username;
        }
    }
}
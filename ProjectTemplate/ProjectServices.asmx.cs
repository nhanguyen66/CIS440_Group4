using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.Services;
using MySql.Data;
using MySql.Data.MySqlClient;
using System.Data;

namespace ProjectTemplate
{
	[WebService(Namespace = "http://tempuri.org/")]
	[WebServiceBinding(ConformsTo = WsiProfiles.BasicProfile1_1)]
	[System.ComponentModel.ToolboxItem(false)]
	[System.Web.Script.Services.ScriptService]

	public class ProjectServices : System.Web.Services.WebService
	{
		////////////////////////////////////////////////////////////////////////
		///replace the values of these variables with your database credentials
		////////////////////////////////////////////////////////////////////////
		private string dbID = "cis440template";
		private string dbPass = "!!Cis440";
		private string dbName = "cis440template";
		////////////////////////////////////////////////////////////////////////
		
		////////////////////////////////////////////////////////////////////////
		///call this method anywhere that you need the connection string!
		////////////////////////////////////////////////////////////////////////
		private string getConString() {
			return "SERVER=107.180.1.16; PORT=3306; DATABASE=" + dbName+"; UID=" + dbID + "; PASSWORD=" + dbPass;
		}
		////////////////////////////////////////////////////////////////////////



		/////////////////////////////////////////////////////////////////////////
		//don't forget to include this decoration above each method that you want
		//to be exposed as a web service!
		[WebMethod(EnableSession = true)]
		/////////////////////////////////////////////////////////////////////////
		public string TestConnection()
		{
			try
			{
				string testQuery = "select * from test";

                string sqlConnectString = System.Configuration.ConfigurationManager.ConnectionStrings["myDB"].ConnectionString;
                ////////////////////////////////////////////////////////////////////////
                MySqlConnection sqlConnection = new MySqlConnection(sqlConnectString);
                string sqlSelect = "SELECT * from USERS";


                MySqlCommand sqlCommand = new MySqlCommand(sqlSelect, sqlConnection);
                //a data adapter acts like a bridge between our command object and 
                //the data we are trying to get back and put in a table object
                MySqlDataAdapter sqlDa = new MySqlDataAdapter(sqlCommand);

                DataTable table = new DataTable();
                sqlDa.Fill(table);
				return "Success!";
			}
			catch (Exception e)
			{
				return "Something went wrong, please check your credentials and db name and try again.  Error: "+e.Message;
			}
		}

        [WebMethod(EnableSession = true)]
        public string CreateUser(string firstName, string lastName, string email, string userName, string password)
        {
            string sqlConnectString = System.Configuration.ConfigurationManager.ConnectionStrings["myDB"].ConnectionString;

            string insertUser = "insert into USERS" +
                "(USER_NAME, PASSWORD, FIRST_NAME, LAST_NAME, EMAIL)" +
                " VALUES " +
                 "(@username,@password, @firstName, @lastName,@email);" +
                "SELECT USER_ID FROM USERS ORDER BY JOIN_DATE DESC LIMIT 1;";

            MySqlConnection sqlConnection = new MySqlConnection(sqlConnectString);
            MySqlCommand sqlCommand = new MySqlCommand(insertUser, sqlConnection);

            sqlCommand.Parameters.AddWithValue("@username", HttpUtility.UrlDecode(userName));
            sqlCommand.Parameters.AddWithValue("@password", HttpUtility.UrlDecode(password));
            sqlCommand.Parameters.AddWithValue("@firstName", HttpUtility.UrlDecode(firstName));
            sqlCommand.Parameters.AddWithValue("@lastName", HttpUtility.UrlDecode(lastName));
            sqlCommand.Parameters.AddWithValue("@email", HttpUtility.UrlDecode(email));


            int accountID;

            sqlConnection.Open();
            try
            {
                accountID = Convert.ToInt32(sqlCommand.ExecuteScalar());
            }
            catch (Exception ex)
            {
                return ex.ToString();
            }

            return accountID.ToString(); 
        }


        [WebMethod(EnableSession = true)]
        public string AddArt(string userEmail, string url, string title, string description, string price)
        {
            string sqlConnectString = System.Configuration.ConfigurationManager.ConnectionStrings["myDB"].ConnectionString;
            string getUser = "SELECT USER_ID FROM USERS WHERE USER_NAME = @userEmail";
            string insertArt = "insert into ART" +
                "(USER_ID, TITLE, DESCRIPTION, PRICE, URL)" +
                " VALUES " +
                 "(@userID, @title, @description, @price, @url);" +
                "SELECT TITLE FROM ART ORDER BY POST_DATE DESC LIMIT 1;";

            MySqlConnection sqlConnection = new MySqlConnection(sqlConnectString);
            MySqlCommand getUserCommand = new MySqlCommand(getUser, sqlConnection);
            MySqlCommand insertArtCommand = new MySqlCommand(insertArt, sqlConnection);

            getUserCommand.Parameters.AddWithValue("@userEmail", HttpUtility.UrlDecode(userEmail));

            insertArtCommand.Parameters.AddWithValue("@url", HttpUtility.UrlDecode(url));
            insertArtCommand.Parameters.AddWithValue("@title", HttpUtility.UrlDecode(title));
            insertArtCommand.Parameters.AddWithValue("@description", HttpUtility.UrlDecode(description));
            insertArtCommand.Parameters.AddWithValue("@price", HttpUtility.UrlDecode(price));

            int userID;
            string returnTitle;

            sqlConnection.Open();
            try
            {
                userID = Convert.ToInt32(getUserCommand.ExecuteScalar());
                insertArtCommand.Parameters.AddWithValue("@userID", userID);
                try
                {
                    returnTitle = Convert.ToString(insertArtCommand.ExecuteScalar());
                }
                catch (Exception ex)
                {
                    return ex.ToString();
                }

            }
            catch (Exception ex)
            {
                return "Wrong email address";
            }

            return returnTitle;
        }
    }
}

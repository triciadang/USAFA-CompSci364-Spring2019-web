<?php

  // retrieve session information
  session_start();

  // if no username set, then redirect to login
  if(!isset($_SESSION['myusername'])){
    header("location:login.php");
    exit;
  }
?>
<html xml:lang="en">
  <head>
    <title>Cadet Service Learning Program</title>
    <link type="text/css" rel="stylesheet" href="csl.css">

    <!-- Set up style for form error feedback areas -->

    <style type="text/css">
      .formError { color: red; font-weight: bold }
    </style>

    <!-- JavaScript for login form data validation -->

    <script type="text/javascript">

      function verifyUpdate()  // used to housekeep when Update User is pressed
      {
        document.getElementById('newUserFormFeedback').innerHTML = "";
        document.getElementById('deleteUserFormFeedback').innerHTML = "";
        document.getElementById('updateUserFormFeedback').innerHTML = "";
        return true;
      }

      function verifyDelete()  // used to housekeep and confirm on Delete User
      {
        document.getElementById('newUserFormFeedback').innerHTML = "";
        document.getElementById('deleteUserFormFeedback').innerHTML = "";
        document.getElementById('updateUserFormFeedback').innerHTML = "";
        var result=confirm("Are you sure you want to delete this user?");
        if (result==false) 
          document.getElementById('deleteUserFormFeedback').innerHTML = "User not deleted.";
        return result;
      }


      function checkNewUserForm()  // used to housekeep and verify for Create User
      {

        // clear old feedback

        document.getElementById('newUserFormFeedback').innerHTML = "";
        document.getElementById('deleteUserFormFeedback').innerHTML = "";
        document.getElementById('updateUserFormFeedback').innerHTML = "";
 
        // get form values

        var newUsernameValue = document.forms["new_user_form"]["newUsername"].value;
        var newPasswordValue = document.forms["new_user_form"]["newPassword"].value;
        var newPasswordRepeatValue = document.forms["new_user_form"]["newPasswordRepeat"].value;

        if (newUsernameValue == "")
        {
          document.getElementById('newUserFormFeedback').innerHTML = 
                     "ERROR: Must specify a username."
          return false;
        }

        if (newPasswordValue == "")
        {
          document.getElementById('newUserFormFeedback').innerHTML = 
                     "ERROR: Must specify a password."
          return false;
        }

        if (newPasswordValue != newPasswordRepeatValue)
        {
          document.getElementById('newUserFormFeedback').innerHTML = 
                     "ERROR: Passwords must match."
          return false;
        }

	return true;

      }
    </script>		
  </head>

<!-- ************************** Begin HTML Body ************************************ -->

  <body>
    <table border="0" width="100%">
      <tbody>
        <tr>
          <td colspan="4"><div id="csl_site_title" ><br/> 
            <center>Cadet Service Learning (CSL) Program</center><br /></div>
          </td>
        </tr>
        <tr>
          <td width="25%"><center><div id="csl_navigation">
            <a href="index.html">Introduction</a></div></center></td>
          <td width="25%"><center><div id="csl_navigation">
            <a href="partners.php">Service Partners</a></div></center></td>
          <td width="25%"><center><div id="csl_navigation">
            <a href="volunteer.html">Information Form</a></div></center></td>
          <td width="25%"><center><div id="csl_navigation">
            <a href="admin.php">Administration</a></div></center></td>
        </tr>
        <tr>
          <td colspan="4">
            <div id="csl_page_title"><br /><p><center>CSL Admin User Form</center></p></div>
            <center><em><font color="blue">Welcome, 
              <?php echo $_SESSION['myusername'].'.<br/>'; ?></font></em></center>
            <center>

<!-- ************************** Create User Form ************************************ -->

              <hr>
              <form name="new_user_form" method="post" id="new_user_form" 
                    action="create_user.php" onsubmit="return checkNewUserForm()">
                <table border="0" cellpadding="3" cellspacing="1">
                  <tr>
                    <td colspan="2">
                      <center>
                      <div id="newUserFormFeedback" class="formError">
                        <?php 
                          if (isset($_GET['newUserError'])) 
                             {echo 'ERROR: New user not created.'; }
                          if (isset($_GET['newUserSuccess'])) 
                             {echo '<font color="green">New user was created.</font>'; }
                        ?>
                      </div>
                      </center>
                    </td>
                  </tr>
                  <tr>
                    <td>Username</td>
                    <td><input name="newUsername" type="text" id="newUsername"></td>
                  </tr>
                  <tr>
                    <td>Password</td>
                    <td><input name="newPassword" type="password" id="newPassword"></td>
                  </tr>
                  <tr>
                    <td>Repeat Password</td>
                    <td><input name="newPasswordRepeat" type="password" id="newPasswordRepeat"></td>
                  </tr>
                  <tr>
                    <td colspan="2"><br/>
                      <center><input type="submit" name="Submit" value="Create User"></center>
                    </td>
                  </tr>
                </table>
              </form>

<!-- ************************** Update User Form ************************************ -->

              <hr>
              <form name="update_user_form" method="post" id="update_user_form" 
                    action="update_user.php" onsubmit="return verifyUpdate()">
                <table border="0" cellpadding="3" cellspacing="1">
                  <tr>
                    <td colspan="3">
                      <center>
                      <div id="updateUserFormFeedback" class="formError">
                        <?php 
                          if (isset($_GET['updateUserError'])) 
                             {echo 'ERROR: User could not be updated.'; }
                          if (isset($_GET['updateUserSuccess'])) 
                             {echo '<font color="green">Selected user was updated.</font>'; }
                        ?>
                      </div>
                      </center>
                    </td>
                  </tr>
                  <tr>
                    <td>Select User: </td>
                    <td>
                      <select name="user">
                        <?php include('build_user_select.php'); ?>
                      </select>
                    </td>
                    <td>
                      <center><input type="submit" name="Submit" value="Update User"></center>
                    </td>
                  </tr>
                </table>
              </form>

<!-- ************************** Delete User Form ************************************ -->

              <hr>
              <form name="delete_user_form" method="post" id="delete_user_form" 
                    action="delete_user.php" onsubmit="return verifyDelete()">
                <table border="0" cellpadding="3" cellspacing="1">
                  <tr>
                    <td colspan="3">
                      <center>
                      <div id="deleteUserFormFeedback" class="formError">
                        <?php 
                          if (isset($_GET['deleteUserError'])) 
                             {echo 'ERROR: User could not be deleted.'; }
                          if (isset($_GET['deleteUserSuccess'])) 
                             {echo '<font color="green">Selected user was deleted.</font>'; }
                        ?>
                      </div>
                      </center>
                    </td>
                  </tr>
                  <tr>
                    <td>Select User: </td>
                    <td>
                      <select name="user">
                        <?php include('build_user_select.php'); ?>
                      </select>
                    </td>
                    <td>
                      <center><input type="submit" name="Submit" value="Delete User"></center>
                    </td>
                  </tr>
                </table>
              </form>

<!-- ************************** Logout Form ************************************ -->

              <hr>
              <form name="logout_form" method="post" id="logout_form" action="logout.php">
                <input type="Submit" name="Submit" value="Logout">
              </form>
            </center>
          </td>
        </tr>
      </tbody>
    </table>
  </body>
</html>

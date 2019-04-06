
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html>

<!-- partners.php-->
<!-- Shows how to retrieve data with SQL using PHP -->

<html xml:lang="en">
  <head>
    <title>Cadet Service Learning Program</title>
    <link type="text/css" rel="stylesheet" href="csl.css">
		
<!-- Set up style for form error feedback areas -->
    <style type="text/css">
      .formError { color: red; font-weight: bold }
    </style>
	
	<script type="text/javascript" src="script.js"></script>
  </head>

 <body>
   <table border="0" width="100%">
     <tbody>
       <tr>
	 <td colspan="4"><div id="csl_site_title" ><br /><center>Cadet Service Learning (CSL) Program</center><br /></div></td>
       </tr>
       <tr>
         <td width="33%"><center><div id="csl_navigation"><a href="index.html">Introduction</a></div></center></td>
         <td width="33%"><center><div id="csl_navigation"><a href="partners.php">Service Partners</a></div></center></td>
         <td width="33%"><center><div id="csl_navigation"><a href="volunteer.html">Information Form</a></div></center></td>
       </tr>
       <tr>
	 <td colspan="4">
           <div id="csl_page_title">
             <br /><p><center>CSL Service Partners (SQL Retrieval Demo)</center><p>
           </div>
           <center>
           <table border="1" cellpadding="4">
             <th>Service Partner Name</th><th>Location</th><th>Phone</th>

<!-- Note the use of <?php ?> to embed PHP commands 
     and connect to the database and retrieve the info -->

             <?php 

             // open connection to the database on LOCALHOST with 
             // userid of 'root', password '', and database 'csl'

             @ $db = new mysqli('LOCALHOST', 'root', '', 'csl');

             // Check if there were error and if so, report and exit

             if (mysqli_connect_errno()) 
             { 
               echo 'ERROR: Could not connect to database.  Error is '.mysqli_connect_error();
               exit;
             }

             // run the SQL query to retrieve the service partner info

             $results = $db->query('SELECT * FROM PARTNERS');

             // determine how many rows were returned

             $num_results = $results->num_rows;

             // loop through each row building the table rows and data columns

             for ($i=0; $i < $num_results; $i++) 
             {
               $r= $results->fetch_assoc();
               print '<tr><td>'.$r['partnerName'].'</td><td>'.$r['partnerLocation'].'</td><td>'.$r['partnerPhone'].' </td></tr>';
             }

             // deallocate memory for the results and close the database connection

             $results->free();
             $db->close();

           ?>
           </table>
           </center>
           <br />
         </td>
       </tr>
     </tbody>
   </table>
 </center> 
 </body>
</html> 
# SMARTShoppingCart
 ESP32 based SMART Shopping Cart that scans barcodes

 <b>Frontend :</b> HTML/CSS, Javascript (Ajax) </br>
 <b>Backend :</b> Python </br>
 <b>Routing API's :</b> Flask framework </br>
 <b>Database :</b> MySQL </br>
 <b>Login :</b> OAuth </br>
 <b>Libraries :</b> Zbar (python) </br>
 <b>Hosted :</b> AWS EC2 </br>

Checkout the working here! - http://shoppingcart.anaghascu.com/login

The primary objective of this project was to leverage the capabilities of the cost-effective yet highly functional ESP32 microprocessor and develop web APIs. By combining the ESP32 microprocessor with the ESP32-CAM module, I was able to create a barcode scanner that seamlessly displays the selected product on the website, offering a powerful and efficient solution to the problem of long queueing lines at counters.

Using the ESP32 microprocessor, the system captures an image of the barcode, which is then converted into JSON format. The resulting data is transmitted as a POST request to the "/cart" API endpoint of the Flask-based web server. At the server, the JSON is decoded and processed by the Zbar library to extract the UPC code of the item, which is then added to the shopping cart of the authenticated user. The system stores all the items in the cart to a MySQL database, which gets cleared when the user clicks on the checkout button. The User can also delete an item which clears the item from the users cart. To ensure a seamless user experience, the system employs Ajax to update the cart's contents from the database every 5 seconds. 

#Login Page

#User Authentication using OAuth

#Home Screen

#User cart

#On Deletion

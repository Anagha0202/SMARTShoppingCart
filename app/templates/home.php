<!DOCTYPE html>
<html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Home - SMART Shopping Cart</title>

    <script src="https://cdn.bootcss.com/popper.js/1.12.9/umd/popper.min.js"></script>
    <script src="https://cdn.bootcss.com/jquery/3.3.1/jquery.min.js"></script>
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/js/bootstrap.bundle.min.js"></script>


    <!--<link rel="stylesheet" type="text/css" href="main.css">
    <script src="main.js"></script> -->

    <link href="{{ url_for('static', filename='css/main.css') }}" rel="stylesheet"> 
    <script src="{{ url_for('static', filename='js/main.js') }}" type ="text/javascript"></script>
    </head>

    <body>
        {% if google_data %}
        <div id="header">
            <nav class="navbar navbar-expand-sm">
		<div class="container-fluid">
		   <figure>
		    <a class="navbar-brand" href="./" id="img-logo"><img id="img-logo" src="/static/css/shoppingCartLogo.png"></img></a>
		   </figure>
                
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#collapsibleNavbar">
                        <span class="navbar-toggler-icon"></span>
                    </button>

                    <div class="collapse navbar-collapse" id="collapsibleNavbar">
                        <ul class="navbar-nav">
                            <li class="nav-item">
                                <a class="nav-link" href="/mycart">{{ google_data.name}}'s Cart</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="#">About Us</a>
                            </li>
                            <li class="nav-item">
                                <a class="nav-link" href="./logout"><button type="button" class="btn btn-outline-light btn-block" id="btn-logout"style="font-size: 25px;">Logout</button></a>
                            </li>
                        </ul>
                    </div>
                </div>
            </nav>
        </div>

        <div class="container">
            <div class="inner-container">
                <article class="row">
                    <h2></h2>
                    <article class="col-sm-1"><h2></h2></article>
                    <article class="col-sm-3" id="hiSymbol"> <h2></h2>
                        <p>&#128075;&#127996;</p>
                    </article>
                    <article class="col-sm-7" id="hiText"> <h2></h2>
                        <p>Hi {{ google_data.name }}, <br>Welcome to the <b>SMART Shopping cart</b>.</p>
                    </article>
                </article>
                <article class="row">
                    <article class="col-sm-2"></article> 
                    <article class="col-sm-3" id="shopSymbol"><p>&#128722</p></article>
                    <article class="col-sm-4" id="shopText">
                        Start Shopping! 
                    </article>
                    <article class="col-sm-3">
                        <button type="button" class="btn btn-info btn-block" id="btn-cart">Add items to your cart!</button>
                    </article>
                </article>
            </div>
        </div>

        <div id="footer">
	    <div class="container-fluid">
		<p style="color: whitesmoke; text-align:center; font-size:25px;">
			Thank You!
		</p>
                <!--<article class="marquee"> 
                    Group: Breadboard - Smart Shopping Cart | Team members: Manoj Athreya, Sathvik Basavaraju, Sudhanva Aithal, Anagha Viswanath
                </article>-->
            </div>
        </div>
        {% endif %}
    </body>
</html>

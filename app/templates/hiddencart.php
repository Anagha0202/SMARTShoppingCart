<label id="value_lable">

  {% if not upc|length  %}
  <h2>Cart is empty. Please add items to cart.</h2>
  {% else %}
<form method="post" action="/mycart">
    <table class="styled-table">
      <thead>
        <tr>
            <th>Item</th>
            <th>UPC</th>
            <th>Product Name</th>
            <th>Price</th>
            <th>Quantity</th>
	    <th>Delete Item</th>
        </tr>
    </thead>
    <tbody>
        {% for i in upc %}
        <tr>
            <td>{{loop.index}}</td>
            <td>{{upc[loop.index-1]}}</td>
            <td>{{pname[loop.index-1]}}</td>
            <td>{{price[loop.index-1]}}</td>
            <td>{{quantity[loop.index-1]}}</td>
            <td><center><button type="submit" class="button" name="deleteItem" value={{upc[loop.index-1]}}>-</button></center></td>
        </tr>{% endfor %}
    </tbody>
</table>
</form>
{% endif %}
</label>

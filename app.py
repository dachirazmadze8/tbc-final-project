from ext import app
from routes import home,about,products,search,create_product,edit_product,delete_product,product_details,rate_product,add_to_cart,view_cart,remove_from_cart,register,login,logout,error,error2



app.run(debug=True,host="0.0.0.0")



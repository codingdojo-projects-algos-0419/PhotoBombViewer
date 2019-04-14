from config import app
from controller_functions import index, register, login, show_dashboard, process_new_user, \
    show_login_page, users_logout, upload_file, show_upload_page, uploaded_file, \
    show_edit_page, update_photo_info, delete_photo

app.add_url_rule("/", view_func=index)
app.add_url_rule("/register", view_func=register)

app.add_url_rule("/login", view_func=show_login_page)
app.add_url_rule("/login_user", view_func=login, methods=["POST"])
app.add_url_rule("/logout", view_func=users_logout, methods=["GET"])

app.add_url_rule("/addUser", view_func=process_new_user)
app.add_url_rule("/process_new_user", view_func=process_new_user, methods=["POST"])

app.add_url_rule("/dashboard", view_func=show_dashboard)
app.add_url_rule("/upload", view_func=show_upload_page)
app.add_url_rule("/upload_file", view_func=upload_file, methods=["POST"])
app.add_url_rule("/uploaded/<filename>", view_func=uploaded_file)


app.add_url_rule("/edit_photo/<id>", view_func=show_edit_page)
app.add_url_rule("/delete_photo/<id>", view_func=delete_photo)

app.add_url_rule("/update_photo_info/<id>", view_func=update_photo_info, methods=["POST"])


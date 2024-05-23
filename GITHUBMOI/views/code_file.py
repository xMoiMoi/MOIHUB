from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
import sirope
from model.code_file import CodeFile
from model.comment import Comment

code_file_blpr = Blueprint('code_file', __name__, url_prefix='/code_file')

@code_file_blpr.route('/my_codes', methods=["GET"])
@login_required
def my_code_files():
    srp = sirope.Sirope()
    user_email = current_user.email
    code_files = list(srp.filter(CodeFile, lambda cf: cf.user_email == user_email))
    return render_template('my_code_files.html', code_files=code_files, srp=srp)

@code_file_blpr.route('/add', methods=["GET", "POST"])
@login_required
def add_code_file():
    if request.method == "POST":
        srp = sirope.Sirope()
        name = request.form.get("name", "").strip()
        content = request.form.get("content", "").strip()
        language = request.form.get("language", "").strip()
        user_email = current_user.email

        if name and content and language:
            code_file = CodeFile(user_email, name, content, language)
            srp.save(code_file)
            flash("Archivo de código añadido con éxito", "success")
            return redirect(url_for('dashboard'))  # Redirige a la página principal después de añadir el código

    return render_template('add_code_file.html')

@code_file_blpr.route('/edit/<safe_code_id>', methods=["GET", "POST"])
@login_required
def edit_code_file(safe_code_id):
    srp = sirope.Sirope()
    code_id = srp.oid_from_safe(safe_code_id)
    code_file = srp.load(code_id)

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        content = request.form.get("content", "").strip()
        language = request.form.get("language", "").strip()

        if name and content and language:
            code_file.name = name
            code_file.content = content
            code_file.language = language
            srp.save(code_file)
            flash("Archivo de código actualizado con éxito", "success")
            return redirect(url_for('code_file.my_code_files'))

    return render_template('edit_code_file.html', code_file=code_file, srp=srp)

@code_file_blpr.route('/delete/<safe_code_id>', methods=["POST"])
@login_required
def delete_code_file(safe_code_id):
    srp = sirope.Sirope()
    code_id = srp.oid_from_safe(safe_code_id)
    srp.delete(code_id)
    flash("Archivo de código eliminado con éxito", "success")
    return redirect(url_for('code_file.my_code_files'))

@code_file_blpr.route('/view/<safe_code_id>', methods=["GET", "POST"])
@login_required
def view_code_file(safe_code_id):
    srp = sirope.Sirope()
    code_id = srp.oid_from_safe(safe_code_id)
    code_file = srp.load(code_id)
    comments = list(srp.filter(Comment, lambda c: c.code_file_id == code_id))

    if request.method == "POST":
        content = request.form.get("content", "").strip()
        if content:
            comment = Comment(current_user.email, code_id, content)
            srp.save(comment)
            flash("Comentario añadido con éxito", "success")
            return redirect(url_for('code_file.view_code_file', safe_code_id=safe_code_id))

    return render_template('view_code_file.html', code_file=code_file, comments=comments, srp=srp)

@code_file_blpr.route('/add_comment/<safe_code_id>', methods=["POST"])
@login_required
def add_comment(safe_code_id):
    srp = sirope.Sirope()
    code_id = srp.oid_from_safe(safe_code_id)
    content = request.form.get("content", "").strip()

    if content:
        comment = Comment(current_user.email, code_id, content)
        srp.save(comment)
        flash("Comentario añadido con éxito", "success")

    return redirect(url_for('code_file.view_code_file', safe_code_id=safe_code_id))

@code_file_blpr.route('/favorite/<safe_code_id>', methods=["POST"])
@login_required
def toggle_favorite(safe_code_id):
    srp = sirope.Sirope()
    code_id = srp.oid_from_safe(safe_code_id)
    code_file = srp.load(code_id)
    if code_file:
        code_file.is_favorite = not code_file.is_favorite
        srp.save(code_file)
        flash("Favorite status updated.", "success")
    else:
        flash("Code file not found.", "error")
    return redirect(url_for('dashboard'))

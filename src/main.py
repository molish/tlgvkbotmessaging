from flask import Blueprint, render_template, request, flash, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy.testing import in_

from .models import *

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/workallusers')
@login_required
def workallusers():
    users = User.query.all()
    relations = db.session.query(users_groups_relations).all()
    groups = Group.query.all()
    return render_template('workallusers.html', users=users, groups=groups, relations=relations)


@main.route('/workallgroups')
@login_required
def workallgroups():
    users = User.query.all()
    relations = db.session.query(users_groups_relations).all()
    groups = Group.query.all()
    return render_template('workallgroups.html', users=users, groups=groups, relations=relations)


@main.route('/creategroup')
@login_required
def creategroup():
    return render_template('creategroup.html')


@main.route('/creategroup', methods=['POST'])
@login_required
def creategroup_post():
    group_name = request.form.get('group_name')
    if not group_name:
        flash('Имя группы не может быть пустым')
        return redirect(url_for('main.creategroup'))
    else:
        group = Group(name=group_name, owner_id=current_user.id)
        db.session.add(group)
        db.session.commit()
    return redirect(url_for('main.workallgroups'))


@main.route('/<int:id>/editgroup')
@login_required
def editgroup(id):
    group = Group.query.filter_by(id=id).first()
    owner = User.query.filter_by(id=group.owner_id).first()
    relations = db.session.query(users_groups_relations).filter_by(group_id=group.id)
    group_users = []
    for row in relations:
        group_users.append(row.user_id)
    users = User.query.filter(User.id.in_(group_users)).all()
    not_in_group = User.query.filter(User.id.not_in(group_users)).all()
    return render_template('editgroup.html', group=group, owner=owner, users=users, not_in_group=not_in_group)


@main.route('/<int:id>/editgroup', methods=['POST'])
@login_required
def editgroup_post(id):
    new_group_name = request.form.get('new_group_name')
    if not new_group_name:
        flash('Имя группы не может быть пустым')
    else:
        Group.query.filter_by(id=id).update({'name': new_group_name})
        db.session.commit()
    return redirect(url_for('main.editgroup', id=id))


@main.route('/<int:id>/deletegroup')
@login_required
def deletegroup(id):
    Group.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Группа удалена')
    return redirect(url_for('main.workallgroups'))
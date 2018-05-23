from flask import Blueprint, render_template, redirect

blueprint = Blueprint('blueprint', __name__, template_folder='templates')


@blueprint.route('/', defaults={'page': 'index'})
@blueprint.route('/<page>')
def show(page):
    return render_template('{}.html'.format(page))


@blueprint.route('/learnSentences')
def learn_sentences():
    return redirect('/')

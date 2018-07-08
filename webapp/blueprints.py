from flask import Blueprint, render_template, redirect

blueprint = Blueprint('blueprint', __name__, template_folder='templates')


@blueprint.route('/', defaults={'page': 'learnSentences'})
@blueprint.route('/<page>')
def show(page):
    return render_template('{}.html'.format(page))


@blueprint.route('/exploreHanzi')
def learn_hanzi():
    return redirect('/progress')


@blueprint.route('/recent')
def recent_items():
    return redirect('/clipboard')

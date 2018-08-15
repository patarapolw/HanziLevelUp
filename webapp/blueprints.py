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


@blueprint.route('/editor/<item_type>')
def editor(item_type):
    from webapp.databases import SrsTuple

    config = {
        'colHeaders': SrsTuple.__slots__,
        'renderers': {
            'front': 'markdownRenderer',
            'back': 'markdownRenderer'
        },
        'colWidths': [210, 579, 155, 85, 220]
    }

    return render_template('editor.html',
                           title=item_type, itemType=item_type, config=config)

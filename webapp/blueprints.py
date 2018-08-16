from flask import Blueprint, render_template, redirect, Response

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


@blueprint.route('/card/<item_type>/<int:card_id>')
def card(item_type, card_id):
    from webapp.databases import Hanzi, Vocab, Sentence, SrsTuple

    if item_type == 'hanzi':
        SrsRecord = Hanzi
    elif item_type == 'vocab':
        SrsRecord = Vocab
    elif item_type == 'sentences':
        SrsRecord = Sentence
    else:
        return Response(status=404)

    record = SrsRecord.query.filter_by(id=card_id).first()
    return render_template('card.html', card=SrsTuple.from_db(record), show=False)


@blueprint.route('/card/<item_type>/<int:card_id>/show')
def card_show(item_type, card_id):
    from webapp.databases import Hanzi, Vocab, Sentence, SrsTuple

    if item_type == 'hanzi':
        SrsRecord = Hanzi
    elif item_type == 'vocab':
        SrsRecord = Vocab
    elif item_type == 'sentences':
        SrsRecord = Sentence
    else:
        return Response(status=404)

    record = SrsRecord.query.filter_by(id=card_id).first()
    return render_template('card.html', card=SrsTuple.from_db(record), show=True)

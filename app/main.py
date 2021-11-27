import json
from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


SQLALCHEMY_DATABASE_URL = 'mysql://root:root@db/wanted'

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL
# )
#
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)

db = SQLAlchemy(app)


@app.route('/search')
def company_name_autocomplete():
    query = request.args.get('query')
    language = request.headers.get('x-wanted-language')

    return 'search'


@app.route('/companies/<company_name>')
def company_search(company_name):
    print(company_name)
    language = request.headers.get('x-wanted-language')

    return 'company_search'


@app.route('/companies', methods=['POST'])
def new_company():
    language = request.headers.get('x-wanted-language')
    print(request.get_json())
    # company_name = data.get('company_name', {})
    # tag_list = data.get('tags', [])
    # language_list = list(company_name.keys())

    return 'test'
    # company = Company()
    #
    # for i in range(len(tag_list)):
    #     tag_id = tag_list[i]['tag_name'][language_list[0]].split('_')[1]
    #
    #     if not Tag.objects.filter(id=tag_id).exists():
    #         Tag.objects.create(id=tag_id)
    #
    #     CompanyTag.objects.create(
    #         company=company,
    #         tag_id=tag_id
    #     )
    #
    # for type in language_list:
    #     language_type, is_language_type = LanguageType.objects.get_or_create(
    #         type=type
    #     )
    #     CompanyName.objects.create(
    #         company=company,
    #         language_type=language_type,
    #         name=company_name[type]
    #     )
    #
    #     for i in range(len(tag_list)):
    #         tag_id = tag_list[i]['tag_name'][type].split('_')[1]
    #
    #         TagName.objects.get_or_create(
    #             tag_id=tag_id,
    #             language_type=language_type,
    #             name=tag_list[i]['tag_name'][type]
    #         )
    #
    # if not LanguageType.objects.filter(type=language).exists():
    #     # return abort(404, 'LANGUAGE_TYPE_DOES_NOT_EXIST')
    #     return jsonify({'message': 'LANGUAGE_TYPE_DOES_NOT_EXIST'}, status=404)
    #
    # language_type = LanguageType.objects.get(type=language)
    # company_name = CompanyName.objects.get(company=company, language_type=language_type)
    # tags = CompanyTag.objects.select_related('tag').filter(company=company)
    # tag_id_list = [tag.tag_id for tag in tags]
    # tag_names = TagName.objects.filter(tag_id__in=tag_id_list, language_type=language_type)
    # result = {"company_name": company_name.name,
    #           "tags": [tag.name for tag in tag_names]
    #           }
    #
    # return jsonify({'data': result}, status=201)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

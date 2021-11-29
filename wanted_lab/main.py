from flask_cors import CORS
from flask import Flask, jsonify, abort, request
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = 'mysql://root:root@db/wanted'

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
db = SQLAlchemy()
db.init_app(app)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


@dataclass
class Company(db.Model):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100))

    company_names = relationship("CompanyName", back_populates="company")
    company_tags = relationship("CompanyTag", back_populates="company")


@dataclass
class LanguageType(db.Model):
    __tablename__ = "language_types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(100), unique=True, index=True)

    company_names = relationship("CompanyName", back_populates="language_type")
    tag_names = relationship("TagName", back_populates="language_type")


@dataclass
class CompanyName(db.Model):
    __tablename__ = "company_names"

    id = Column(Integer, primary_key=True, index=True)
    language_type_id = Column(Integer, ForeignKey("language_types.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String(100), index=True)
    language_type = relationship("LanguageType", back_populates="company_names")
    company = relationship("Company", back_populates="company_names")


@dataclass
class TagName(db.Model):
    __tablename__ = "tag_names"

    id = Column(Integer, primary_key=True, index=True)
    language_type_id = Column(Integer, ForeignKey("language_types.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    name = Column(String(100), index=True)
    language_type = relationship("LanguageType", back_populates="tag_names")
    tag = relationship("Tag", back_populates="tag_names")


@dataclass
class CompanyTag(db.Model):
    __tablename__ = "company_tags"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    company = relationship("Company", back_populates="company_tags")
    tag = relationship("Tag", back_populates="company_tags")


@dataclass
class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))

    tag_names = relationship("TagName", back_populates="tag")
    company_tags = relationship("CompanyTag", back_populates="tag")


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
    request_language = request.headers.get('x-wanted-language')
    data = request.get_json()
    company_name = data.get('company_name', {})
    tag_list = data.get('tags', [])
    language_list = list(company_name.keys())
    company = Company()

    res_company_name = ''
    res_tag_names = []

    for i in range(len(tag_list)):
        tag_id = tag_list[i]['tag_name'][language_list[0]].split('_')[1]

        # tag = get_or_create(SessionLocal(), Tag(), id=tag_id)
        tag = Tag(id=tag_id)
        company_tag = CompanyTag()
        company_tag.tag = tag
        company_tag.company = company

    for l_type in language_list:
        if l_type == request_language:
            res_company_name = company_name[l_type]

        language_type = LanguageType(type=l_type)
        company_name = CompanyName(
            company=company,
            language_type=language_type,
            name=company_name[l_type]
        )

        for i in range(len(tag_list)):
            tag_id = tag_list[i]['tag_name'][l_type].split('_')[1]

            tag_name = TagName(
                tag_id=tag_id,
                language_type=language_type,
                name=tag_list[i]['tag_name'][l_type]
            )
            res_tag_names.append(tag_name)

    tag_name_list = [tag.name for tag in res_tag_names]
    if not tag_name_list:
        return jsonify({'message': 'NOT_FOUND_TAG_NAME'}, status=404)

    SessionLocal().add(company)
    SessionLocal().commit()

    result = dict(
        company_name=res_company_name,
        tags=tag_name_list
    )

    return jsonify({'data': result}, status=201)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

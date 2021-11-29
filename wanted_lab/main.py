from flask_cors import CORS
from flask import Flask, jsonify, request
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


# TODO: Move models file
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


# TODO: Move views file
@app.route('/search')
def company_name_autocomplete():
    x_wanted_language = request.headers.get('x-wanted-language')

    # TODO: Move services file
    language_id = SessionLocal() \
        .query(LanguageType) \
        .filter(LanguageType.type == x_wanted_language) \
        .value(LanguageType.id)

    company_list = SessionLocal() \
        .query(CompanyName) \
        .filter(CompanyName.language_type_id == language_id) \
        .join(LanguageType, CompanyName.language_type_id == LanguageType.id)

    if x_wanted_language:
        model_column = getattr(CompanyName, "name")
        company_id = SessionLocal() \
            .query(CompanyName) \
            .filter(model_column.ilike(f'{x_wanted_language}%')) \
            .join(LanguageType, CompanyName.language_type_id == LanguageType.id)

        company_id_list = [company.company_id for company in company_id]

        company_list = SessionLocal().query(CompanyName). \
            filter(CompanyName.company_id.in_(company_id_list)). \
            filter(CompanyName.language_type_id == language_id). \
            join(LanguageType, CompanyName.language_type_id == LanguageType.id)

    result = [dict(company_name=company.name) for company in company_list]
    return result


@app.route('/companies/<company_name>')
def company_search(company_name):
    x_wanted_language = request.headers.get('x-wanted-language')

    try:
        # TODO: Move services file
        language_id = SessionLocal() \
            .query(LanguageType) \
            .filter(LanguageType.type == x_wanted_language) \
            .value(LanguageType.id)

        company = SessionLocal() \
            .query(CompanyName) \
            .filter(CompanyName.name == company_name) \
            .join(Company, CompanyName.company_id == Company.id)

        company_name = SessionLocal() \
            .query(CompanyName) \
            .filter(CompanyName.company_id == company.value(CompanyName.company_id), LanguageType.id == language_id) \
            .join(LanguageType, CompanyName.language_type_id == LanguageType.id).value(CompanyName.name)

        lang_tags_set = SessionLocal().query(TagName). \
            filter(TagName.language_type_id == language_id). \
            join(Tag, TagName.tag_id == Tag.id)

        lang_tags_list = [tag.tag_id for tag in lang_tags_set]

        company_tags = SessionLocal().query(CompanyTag)\
            .filter(CompanyTag.company_id == company.value(CompanyName.company_id),
                   CompanyTag.tag_id.in_(lang_tags_list))\
            .join(Tag, CompanyTag.tag_id == Tag.id)

        tag_id_list = [tag.tag_id for tag in company_tags]

        tag_name_list = SessionLocal().query(Tag). \
            filter(Tag.id.in_(tag_id_list))

        tag_result = [tag.name for tag in tag_name_list]

        result = dict(
            company_name=company_name,
            tags=tag_result
        )
        return result

    except AttributeError:
        return jsonify({'message': 'INTERNAL_SERVER_ERROR'}, status=500)


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

    # TODO: Move services file
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

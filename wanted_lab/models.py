from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from sqlalchemy.orm import relationship
from sqlalchemy import Column, ForeignKey, Integer, String

db = SQLAlchemy()


@dataclass
class Company(db.Model):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String(100))

    company_names = relationship("CompanyName", back_populates="company")
    company_tags = relationship("CompanyTag", back_populates="company")

    def __init__(self, company_name, company_names=None, company_tags=None):
        self.company_name = company_name
        self.company_names = company_names
        self.company_tags = company_tags


@dataclass
class LanguageType(db.Model):
    __tablename__ = "language_types"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String(100), unique=True, index=True)

    company_names = relationship("CompanyName", back_populates="language_type")
    tag_names = relationship("TagName", back_populates="language_type")

    def __init__(self, type, company_names=None, tag_names=None):
        self.type = type
        self.company_names = company_names
        self.tag_names = tag_names


@dataclass
class CompanyName(db.Model):
    __tablename__ = "company_names"

    id = Column(Integer, primary_key=True, index=True)
    language_type_id = Column(Integer, ForeignKey("language_types.id"))
    company_id = Column(Integer, ForeignKey("companies.id"))
    name = Column(String(100), index=True)
    language_type = relationship("LanguageType", back_populates="company_names")
    company = relationship("Company", back_populates="company_names")

    def __init__(self, language_type_id, company_id, name, language_type, company):
        self.language_type_id = language_type_id
        self.company_id = company_id
        self.name = name
        self.language_type = language_type
        self.company = company


@dataclass
class TagName(db.Model):
    __tablename__ = "tag_names"

    id = Column(Integer, primary_key=True, index=True)
    language_type_id = Column(Integer, ForeignKey("language_types.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))
    name = Column(String(100), index=True)
    language_type = relationship("LanguageType", back_populates="tag_names")
    tag = relationship("Tag", back_populates="tag_names")

    def __init__(self, language_type_id, tag_id, name, language_type, tag):
        self.language_type_id = language_type_id
        self.tag_id = tag_id
        self.name = name
        self.language_type = language_type
        self.tag = tag


@dataclass
class CompanyTag(db.Model):
    __tablename__ = "company_tags"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    tag_id = Column(Integer, ForeignKey("tags.id"))

    company = relationship("Company", back_populates="company_tags")
    tag = relationship("Tag", back_populates="company_tags")

    def __init__(self, company_id, tag_id, company, tag):
        self.company_id = company_id
        self.tag_id = tag_id
        self.company = company
        self.tag = tag


@dataclass
class Tag(db.Model):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(40))

    tag_names = relationship("TagName", back_populates="tag")
    company_tags = relationship("CompanyTag", back_populates="tag")

    def __init__(self, name, tag_names, company_tags):
        self.name = name
        self.tag_names = tag_names
        self.company_tags = company_tags



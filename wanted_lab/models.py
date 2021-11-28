# # from wanted_lab.database import Base, db
# from wanted_lab.main import db
# from dataclasses import dataclass
# from sqlalchemy.orm import relationship
# from sqlalchemy import Column, ForeignKey, Integer, String
#
#
# @dataclass
# class Company(db.Model):
#     __tablename__ = "companies"
#
#     id = Column(Integer, primary_key=True, index=True)
#     company_name = Column(String(100))
#
#     company_names = relationship("CompanyName", back_populates="company")
#     company_tags = relationship("CompanyTag", back_populates="company")
#
#
# @dataclass
# class LanguageType(db.Model):
#     __tablename__ = "language_types"
#
#     id = Column(Integer, primary_key=True, index=True)
#     type = Column(String(100), unique=True, index=True)
#
#     company_names = relationship("CompanyName", back_populates="language_type")
#     tag_names = relationship("TagName", back_populates="language_type")
#
#
# @dataclass
# class CompanyName(db.Model):
#     __tablename__ = "company_names"
#
#     id = Column(Integer, primary_key=True, index=True)
#     language_type_id = Column(Integer, ForeignKey("language_types.id"))
#     company_id = Column(Integer, ForeignKey("companies.id"))
#     name = Column(String(100), index=True)
#
#     language_type = relationship("LanguageType", back_populates="company_names")
#     company = relationship("Company", back_populates="company_names")
#
#
# @dataclass
# class TagName(db.Model):
#     __tablename__ = "tag_names"
#
#     id = Column(Integer, primary_key=True, index=True)
#     language_type_id = Column(Integer, ForeignKey("language_types.id"))
#     tag_id = Column(Integer, ForeignKey("tags.id"))
#     name = Column(String(100), index=True)
#
#     language_type = relationship("LanguageType", back_populates="tag_names")
#     tag = relationship("Tag", back_populates="tag_names")
#
#
# @dataclass
# class CompanyTag(db.Model):
#     __tablename__ = "company_tags"
#
#     id = Column(Integer, primary_key=True, index=True)
#     company_id = Column(Integer, ForeignKey("companies.id"))
#     tag_id = Column(Integer, ForeignKey("tags.id"))
#
#     company = relationship("Company", back_populates="company_tags")
#     tag = relationship("Tag", back_populates="company_tags")
#
#
# @dataclass
# class Tag(db.Model):
#     __tablename__ = "tags"
#
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(40))
#
#     tag_names = relationship("TagName", back_populates="tag")
#     company_tags = relationship("CompanyTag", back_populates="tag")

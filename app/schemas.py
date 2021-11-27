# from pydantic import BaseModel
#
#
# class CompanyBase(BaseModel) :
#     company_name : str
#
#
# class CompanySearch(CompanyBase) :
#
#     class Config :
#         orm_mode = True
#
#
# class CompanyInfo(CompanyBase) :
#     tags : list
#
#     class Config :
#         orm_mode = True
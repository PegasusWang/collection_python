#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import phonenumbers
from phonenumbers import carrier
from phonenumbers.phonenumberutil import number_type


def validate_phone(phone_number):
    try:
        return carrier._is_mobile(number_type(phonenumbers.parse(phone_number)))
    except Exception:
        return False


class Validator(object):
    EMAIL_PAT = re.compile("^.+\\@[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z0-9]{2,10})$")

    @staticmethod
    def validate_email(email):
        if len(email) >= 6 and (Validator.EMAIL_PAT.match(email) is not None):
            return True
        return False

    @staticmethod
    def validate_email_list(email_list):
        """validate_email_list if all email is valid return True, or False
        """
        if not isinstance(email_list, list):
            email_list = [email_list]
        for email in email_list:
            if not Validator.validate_email(email):
                return False
        return True

    @staticmethod
    def validate_phone(phone_number):
        """validate national phone number
        http://stackoverflow.com/questions/16135069/python-validation-mobile-number
        https://github.com/daviddrysdale/python-phonenumbers

        :param phone_number:
        """
        try:
            return carrier._is_mobile(number_type(
                phonenumbers.parse(phone_number))
            )
        except Exception:
            return False

    @staticmethod
    def validate_phone_list(phone_number_list):
        if not isinstance(phone_number_list, list):
            phone_number_list = [phone_number_list]
        for phone in phone_number_list:
            if not Validator.validate_phone(phone):
                return False
        return True

    @staticmethod
    def validate(data_list, data_type):
        """validate 验证邮箱或者phone数据list是否全部合法。

        :param data_list: ['num1', 'num2']
        :param data_type: 'phone' or 'email'
        """
        data_type_to_func = {
            'email': Validator.validate_email_list,
            'phone': Validator.validate_phone_list,
        }
        func = data_type_to_func[data_type]
        return func(data_list)


if __name__ == '__main__':
    number = "+49 176 1234 5678"
    print validate_phone(number)
    number = "+86 18810564550"
    print validate_phone(number)
    number = "18810564550"
    print validate_phone(number)
    number = "49 176 1234 5678"
    print validate_phone(number)
    number = "86 18810564550"
    print validate_phone(number)
    number = "+86-18810564550"
    print validate_phone(number)
    number = "+86-188 1056 4550"
    print validate_phone(number)

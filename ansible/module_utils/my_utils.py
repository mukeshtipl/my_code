class MyHelper(object):
    def ucase(self,message):
        return message.upper()
if __name__ == '__main__':
    sample_message="HellO wOrld"
    my_helper=MyHelper()
    new_message=my_helper.ucase(sample_message)
    print(new_message)
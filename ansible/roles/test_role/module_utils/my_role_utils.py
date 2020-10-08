class MyRoleHelper(object):
    def lcase(self,message):
        return message.lower()
if __name__ == '__main__':
    sample_message="HellO wOrld"
    my_helper=MyRoleHelper()
    new_message=my_helper.lcase(sample_message)
    print(new_message)
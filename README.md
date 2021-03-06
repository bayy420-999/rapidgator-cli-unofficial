# rapidgator-cli-unofficial

Bismillah, this is my first "working" project, made entirely with Termux + Acode on android.

Thanks to [Juvenal-Yescas](https://github.com/Juvenal-Yescas/mediafire-dl) that inspire me to make this project.

You can use rapidgator features like Login and Download from your terminal, this program also support Batch Download.

I'll add more features like async download, threading and so on in the future.

## Getting Started
### Installation
Download the code:
```
git clone https://github.com/bayy420-999/rapidgator-cli-unofficial
```

Move to project directory:
```
cd rapidgator-cli-unofficial
```

### Setup config.ini file

* Open config.ini file with any text editor you prefer
* Change `email` and `password` with your rapidgator account
* You dont need to set anything in `token` variable, it will automatically filled once you login
* Now set `download_path` to path where you want to store the downloaded file(s)
* You can set `is_batch_download` variable with value `true` or `false`
* If you set `is_batch_download` value with `true` then you need to set `batch_file` value with some txt file that store list of urls, see batch.txt file for example

### Use the program

After you done with config.ini file, then you are ready to use the program
* Goto terminal and type:
```
python3 rapidgator.py
```
you'll get this output:
```
You need to login to get token which will be used to download the file(s), you dont need to generate token everytime you want to download file(s), but remember that the token will expire every few hours.

Choose your option:
1. Login
2. Download

Your answer:
```
* Type 1 to login and get token
output:
```
Token successfully generated! token: <your_token>
Do you want to use this program again? (y/n)
```
* Type y and you'll back to main menu
* Now type 2 to actually download the file(s)

If you set `is_batch_download` variable with value `false` then you will get output like this:
```
Input rapidgator url:
```
You can just input any rapidgator link there

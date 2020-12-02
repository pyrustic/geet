`pip install geet`

[https://github.com/pyrustic/geet](https://github.com/pyrustic/geet)

**Get, install, and run the latest release of a compatible app published on Github**

<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/geet-1.gif" alt="Geet">
    <p align="center">
    geet pyrustic/demo + run
    </p>
</div>


<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/geet-2.gif" alt="Geet">
    <p align="center">
    geet pyrustic/pyrustic + install + run
    </p>
</div>


<div align="center">
    <img src="https://raw.githubusercontent.com/pyrustic/misc/master/media/geet-3.gif" alt="Geet">
    <p align="center">
    How to increase requests rate limit
    </p>
</div>


Use the command `auth` to increase your requests rate limit. You will need a token: read this [article](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token) to learn about the personal access token.

This is still `beta`, quickly built to facilitate the installation of Python desktop application `Pyrustic`. If you don't know what `Pyrustic` is, check its [README](https://github.com/pyrustic/geet). 




<br>
<br>

Do you have published some nice Python desktop application release on Github ?

Let assume that your github profile is `pyrusticfan` with a repository named `disrupt`.
What do you prefer:
- do you want your users to go to RELEASES tab, download the asset, unpack the asset in the right folder then install the app ?

  or just

- `geet pyrusticfan/disrupt`
 

I think that the choice is easy to do.


<br><br>


If you want your users to download and install your application with Geet, follow the next principles:

- your asset should be a zip file;
- that's all.

Also, your asset should respect this structure:
- whatever-asset-name.zip
    - repository-name-here-please
        - contents
        - contents
        - whatever-folder
            - blah blah blah
        - whatever-source-code
        - blah blah blah
        - contents-again
        - optionally: `install.py`
        - AND `__main__.py` as entry point !
        
As you can see, it is important to have your project inside a folder named as your repository. If you use [Pyrustic](https://github.com/pyrustic/pyrustic) to publish your nice Python desktop applications on Github, you won't need to care about this detail.



<br><br>

A better doc will come soon ;)

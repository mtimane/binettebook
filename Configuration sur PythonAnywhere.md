# Configuration de GIT avec Python Anywhere

1. Create a directory, so Git doesn't get messy, and enter it

```bash
    mkdir cours && cd cours
```

2. Start a Git repository

```bash
    git config --global credential.helper store     # Enregistre le mdp en clair
    git init
```

3. Track repository, do not enter subdirectory

```bash
    git remote add -f origin https://url/vers/depot/git/
```

4. Enable the tree check feature

```bash
    git config core.sparseCheckout true
```

5. Create a file in the path: .git/info/sparse-checkout
   That is inside the hidden .git directory that was created
   by running the command: git init
   And inside it enter the name of the sub directory you only want to clone

```bash
    echo '420-05C/Blocs/23 - Hebergement/*' >> .git/info/sparse-checkout
```

6. Download with pull, not clone

```bash
    git pull origin master
```

7. Et pour faire le lien avec PythonAnywhere :

```bash
    cd
    rm -fr mysite
    ln -sf cours/420-05C/Blocs/23\ -\ Hebergement/ ./mysite
```
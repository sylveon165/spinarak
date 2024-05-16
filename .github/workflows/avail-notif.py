name: Availability notification

on:
  workflow_dispatch:

jobs:
  python-selenium:
    permissions:
      contents: write
    runs-on: ubuntu-latest
    steps:
    - name: Checkout
      uses: actions/checkout@v4
    - name: Install dependencies
      run: pip install chromedriver-autoinstaller selenium pyvirtualdisplay
    - name: Run Python Selenium script
      run: |
          python avail-notif.py
          ls -al
    - name: Commit & push screenshot to repo
      run: |
          git config --global user.name '${{github.actor}}'
          git config --global user.email '${{github.actor}}@users.noreply.github.com'
          git add --all
          git commit -am "Screenshot"
          git push

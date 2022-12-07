import wptools

def main():
  page = wptools.page('Gandhi').get_query()
  print(page)


if __name__ == '__main__':
  main()

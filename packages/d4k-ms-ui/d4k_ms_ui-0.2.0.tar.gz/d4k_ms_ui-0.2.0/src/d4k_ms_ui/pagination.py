class Pagination():

  def __init__(self, results, base_url, **kwargs):
    self.page = int(results['page'])
    self.page_size = int(results['size'])
    self.item_count = int(results['count'])
    self.filter = results['filter']
    self.page_count = int(self.item_count / self.page_size)
    if self.item_count % self.page_size > 0:
      self.page_count += 1
    self.base_url = base_url
    self.params = kwargs.get('params', {})
    self.disable_filter = kwargs.get('disable_filter', False)
    self.pages = self.build_page_info()

  def build_page_info(self):
    page_info = []
    self.first_page(page_info)
    for i in range(1, self.page_count + 1):
      link = self.link(i)
      active = ""
      disabled = ""
      display_text = str(i)
      add = True
      if i == self.page:
        active = "active"
      elif i == 1 or i == self.page_count:
        pass
      elif self.page - i > 3:
        if page_info[-1]['text'] == "...":
          add = False
        else:
          display_text = "..."
          link = ""
          disabled = "disabled"
      elif i - self.page > 3:
        if page_info[-1]['text'] == "...":
          add = False
        else:
          display_text = "..."
          link = ""
          disabled = "disabled"
      else:
        pass
      if add:
        page_info.append({ 'link': link, 'active': active, 'text': display_text, 'disabled': disabled })
    self.last_page(page_info)
    return page_info

  def first_page(self, page_info):
    disabled = ""
    if self.page == 1:
      disabled = "disabled"
    page_info.append({ 'link': self.link(self.page - 1), 'active': "", 'text': "&laquo;", 'disabled': disabled })

  def last_page(self, page_info):
    disabled = ""
    if self.page == self.page_count:
      disabled = "disabled"
    page_info.append({ 'link': self.link(self.page + 1), 'active': "", 'text': "&raquo;", 'disabled': disabled })

  def autofocus(self):
    if self.filter == "":
      return ""
    else:
      return "autofocus"

  def filter_disabled(self):
    if self.disable_filter:
      return "disabled"
    else:
      return ""

  def filter_text(self):
    if self.disable_filter:
      return "Search disabled!"
    else:
      return "Begin typing to search ..."

  def link(self, page):
    final_link = "%s?page=%s&size=%s&filter=%s" % (self.base_url, page, self.page_size, self.filter)
    for key, value in self.params.items():
      final_link = "%s&%s=%s" % (final_link, key, value)
    return final_link

  def base_link(self, page, size):
    base_link = "%s?page=%s&size=%s" % (self.base_url, page, size)
    for key, value in self.params.items():
      base_link = "%s&%s=%s" % (base_link, key, value)
    return base_link

  def base_link_with_filter(self, page, size):
    base_link = "%s?page=%s&size=%s&filter=%s" % (self.base_url, page, size, self.filter)
    for key, value in self.params.items():
      base_link = "%s&%s=%s" % (base_link, key, value)
    return base_link

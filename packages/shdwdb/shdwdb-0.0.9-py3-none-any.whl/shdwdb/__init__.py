import json
class Db():
  def __init__(self, name, data={}, default=None, fnts=None):
    self.name = name
    self.data = data
    self.default = default
    self.autosave = False
    self.fnts = fnts

  def save(self, filename_to_save=None):
    if filename_to_save is None:
      if self.fnts is not None:
        filename_to_save = self.fnts
      else:
        raise Exception('need a filename')
    f = open(filename_to_save, 'w')
    f.write(json.dumps(self.data))
    f.close()

  def __str__(self):
    toret = '\x1b[1m\x1b[4m' + self.name + '\n\x1b[0m'
    for data in self.data:
      toret += str(data) + ': \n'
      for data2 in self.data[data]:
        toret += str(data2) + ': ' + str(self.data[data][data2]) + '; '
      toret += '\n--------\n'
    return toret

  def set(self, column, row, value):
    self.data[column][row] = value
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)
    return self

  def delete_item(self, column, row):
    self.data[column][row] = None
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)
    return self

  def delete_column(self, column):
    del self.data[column]
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)
    return self

  def delete_row(self, row):
    for data in self.data:
      del self.data[data][row]
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)
    return self

  def get_value(self, column, row):
    return self.data[column][row]

  def get_column(self, column):
    return self.data[column]

  def get_row(self, row):
    end = {}
    for info in self.data:
      end[info] = self.data[info][row]
    return end

  def add_column(self, name):
    self.data[name] = {}
    dat = self.data
    rownames = list(dat[list(dat.keys())[0]].keys())
    try:
      lstid = list(dat[list(dat.keys())[0]].values())[0]
    except IndexError:
      lstid = 0
    for i in rownames:
      if i == 'id':
        apndval = int(lstid)+1
      else:
        apndval = self.default
      self.data[name][i] = apndval
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)
    return self

  def add_row(self, name):
    for iterr in self.data:
      self.data[iterr][name] = self.default
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)
    return self

  def set_row(self, row, value):
    for data in self.data:
      self.data[data][row] = value
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)

  def set_column(self, column, value):
    for data in self.data[column]:
      if data == 'id':
        continue
      self.data[column][data] = value
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)

  def clear(self):
    for data in self.data:
      for data2 in self.data[data]:
        if data2 != 'id':
          self.data[data][data2] = self.default
    if self.autosave and self.fnts is not None:
      self.save(self.fnts)
    return self

  def __add__(self, value):
    new = self
    if type(value) is not type(new):
      raise ValueError('Invalid operand(+) for types ' + str(type(value)) + ' and ' + str(type(new)))
    for iter in value.data:
      new.data[iter] = value.data[iter]
    return new

  def __iter__(self):
    return iter(self.data)

  def __eq__(self, o):
    return self.__dict__ == o.__dict__

  def __bool__(self):
    return self.data != {}

  def __contains__(self, key):
    return key in self.data

def make(name, column_names=[], row_names=[], defaut_value=None, fnts=None):
  name = str(name)
  column_names = list(column_names)
  row_names = list(row_names)
  db_ = Db(name)
  db_.data = {}
  db_.default = defaut_value
  db_.fnts = fnts
  if 'id' not in row_names:
    row_names.insert(0, 'id')
  ids = 1
  for i in range(0, len(column_names)):
    j = column_names[i]
    db_.data[j] = defaut_value
    rowws = {}
    for k in range(0, len(row_names)):
      m = row_names[k]
      if m == 'id':
        rowws[m] = ids
      else:
        rowws[m] = defaut_value
    ids += 1
    db_.data[j] = rowws
  return db_

def retrieve(name, filename_saved):
  with open(filename_saved, 'r') as f:
    return Db(name, json.loads(f.read()))
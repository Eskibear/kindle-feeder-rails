module Python

  PATH = Rails.root.join('lib', 'scripts')

  def self.exec_file(py, params)
    `python #{PATH.join(py)}.py '#{params}'`
  end

  def self.exec2(py, params)
    `python2 #{PATH.join(py)}.py '#{params}'`
  end

  def self.exec3(py, params)
    `python3 #{PATH.join(py)}.py '#{params}'`
  end
end

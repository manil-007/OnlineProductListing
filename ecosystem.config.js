module.exports = {
  apps : [{
    name   : 'opl api',
    script : './main.py',
    interpreter : 'python3',
    args : '-h',
    autorestart : false,
    watch : true
  }]
}

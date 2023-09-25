# TPM-password

## Автоматизации по созданию и обновлению паролей в TPM

Данные скрипты сменят пароль и в TPM и на хосте. 

**Настройка python**
```
pip install tpm requests
```

**Настройки доступа public_key  и  private_key  лежат  ~/.hmac**

```
url: 'http://localhost/index.php/' # Адрес должен оканчиваться слешем /
public_key: ''
private_key: ''
```

**Список хостов должен лежать в ~/hosts.yml**
```
hosts:
  - 192.168.1.1
  - 192.168.1.2
  - 192.168.1.3
```


**Ansible  необходим для возможности шифрования ~/.hmac и автоматической смены пароля на хосте.**

Зашифровываем файл с private_key public_key
```
ansible-vault create ~/.hmac
```

**Дальнейшие обращение к скрипту будет через плейбуки**
```
ansible-playbook --ask-vault-pass check_pass.yaml
ansible-playbook --ask-vault-pass create_pass.yaml
ansible-playbook --ask-vault-pass update_pass.yaml
```

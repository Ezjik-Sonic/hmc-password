# TPM-password

Автоматизации по созданию и обновлению паролей в TPM

Настройка python
pip install tpm

Настройки доступа public_key  и  private_key  лежат  ~/.hmac
url: 'http://localhost/index.php/' # Адрес должен оканчиваться слешем /
public_key: ''
private_key: ''

Список хостов должен лежать в ~/hosts.yml
hosts:
  - 192.168.1.1
  - 192.168.1.2
  - 192.168.1.3

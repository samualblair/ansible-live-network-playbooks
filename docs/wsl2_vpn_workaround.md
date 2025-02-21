# Helpful Guide for Addressing WSL2 Connectivity

Addressing WSL2 Connectivity issue while using Cisco Secure Connect (Anyconnect)

## WSL2 Problem statment
On wsl2 <code class="language-text">sudo apt update</code> will fail when connected to Cisco Anyconnect VPN but without vpn it works fine. The problem is when you are connected to anyconnect, wsl fails to resolve the DNS. It also has problems routing traffic over the vpn tunnel.

For Example:

```text
Err:1 http://archive.ubuntu.com/ubuntu focal InRelease
  Temporary failure resolving <span class="token string">'archive.ubuntu.com'
Err:2 http://security.ubuntu.com/ubuntu focal-security InRelease
  Temporary failure resolving <span class="token string">'security.ubuntu.com'
Err:3 http://archive.ubuntu.com/ubuntu focal-updates InRelease
  Temporary failure resolving <span class="token string">'archive.ubuntu.com'
Err:4 http://archive.ubuntu.com/ubuntu focal-backports InRelease
  Temporary failure resolving <span class="token string">'archive.ubuntu.com'
Reading package lists<span class="token punctuation">... Done
W: Failed to fetch http://archive.ubuntu.com/ubuntu/dists/focal/InRelease  Temporary failure   resolving <span class="token string">'archive.ubuntu.com'
W: Failed to fetch http://archive.ubuntu.com/ubuntu/dists/focal-updates/InRelease  Temporary   failure resolving <span class="token string">'archive.ubuntu.com'
W: Failed to fetch http://archive.ubuntu.com/ubuntu/dists/focal-backports/InRelease    Temporary failure resolving <span class="token string">'archive.ubuntu.com'
W: Failed to fetch http://security.ubuntu.com/ubuntu/dists/focal-security/InRelease    Temporary failure resolving <span class="token string">'security.ubuntu.com'
W: Some index files failed to download. They have been ignored, or old ones used instead.
```

## The solution

1) 
    Connect Cisco Anyconnect VPN, then open up powershell as Admin and run the following commands to get the all the available DNS/nameservers. Take note of the DNS/namservers will need later.

    ```ps
    Get-DnsClientServerAddress -AddressFamily IPv4 
    Select-Object -ExpandProperty ServerAddresses
    ```
2) 
    Then on the same powershell run the following. This will get the search domain that will need later on with the nameservers above.

    ```ps
    Get-DnsClientGlobalSetting
    Select-Object -ExpandProperty SuffixSearchList
    ```
3) 
    Open up wsl, and run the following commands.

    ```bash
    sudo unlink /etc/resolv.conf # this will unlink the default wsl2 resolv.conf

    # This config will prevent wsl2 from overwritting the resolve.conf file everytime
    # you start wsl2
    cat <<EOF | sudo tee -a /etc/wsl.conf
    [network]
    generateResolvConf = false
    EOF

    cat <<EOF | sudo tee -a /etc/resolv.conf
    nameserver 10.50... # The company DNS/nameserver from the command in step 1
    nameserver 10.50... # The company DNS/nameserver from the command in step 1
    nameserver 8.8.8.8
    nameserver 8.8.4.4
    search this.searchdomain.com # The search domain that we got from step 2
    EOF
    ```
4) 
    Change Cisco Anyconnect metric from default 1 to 6000 inside powershell

    ```ps
    Get-NetAdapter | Where-Object {$_.InterfaceDescription -Match "Cisco AnyConnect"} | Set-NetIPInterface -InterfaceMetric 6000
    ```
5) 
    Restart wsl2 on the same elevated powershell, then you can open up wsl2 and it should connect to the internet.

    ```ps
    Restart-Service LxssManager
    ```

#References
[github.com/microsoft/WSL/issues/5068](https://github.com/microsoft/WSL/issues/5068)

[github.com/microsoft/WSL/issues/4277](https://github.com/microsoft/WSL/issues/4277)

Credit for Blog with this format:
[jamespotz.github.io/blog/how-to-fix-wsl2-and-cisco-vpn](https://jamespotz.github.io/blog/how-to-fix-wsl2-and-cisco-vpn)

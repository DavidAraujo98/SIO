# Project 3

## Summary

Following an attack to the services of UA Pintaresto, the team was solicited to preform an analysis in an attempt to bright to light in what way the services were exploited and what data could have been stollen and/or destroyed.

## Description

Following detection of an intrusion, by the automatic systems employed by UA Pinteresto, the team responsible for security of this company was not certain of what may, or may not, have happen to they're systems.

What this team offers as information is that the VM in service was stopped and recorded a **PCAP file** with the past **traffic to and from the VM**.

For analysis, the UA Pintersto's team offer the following data:

1. Capture of the traffic by the VM in the form of:

   a. PCAP file - **netmon.pcap**

   b. Text file containing the HTTP packages of said capture - **http.txt**

2. A **virtual disk image**, of the operating VM, containing sensitive data about the web application of UA Pintaresto

A careful analysis was preformed in each single file, as to leave no doubts or any unchecked piece of data.

## Exploration and Discovery

Do to the fact that the provided data for analysis is not overwhelming, a file by file discovery was the first step in a multilayered analysis.

This said, the file by file order was the following:

1. netmon.pcap

2. http.txt

3. VDI

This order is not random. Being this a internet service, all the data is transmitted via this mean, and so we found it best to focus our initial efforts in discovering **what was transmitted** between the service and a potential attacker.

This way, we could use de traffic capture file as a sort of a chronological timeline of the entire attack. This proved to be a very fruitful method, and guided our analysis the entire way.

The **http.txt** was mainly used as a mean to further explore the HTTP data exchanged between attacker and server.

## Attacker Actions and Behaviour

To describe the action taken by the attacker, we'll resort to the **MITRE ATT&CK** matrix, witch well describes the complete set os procedures that can used by an attacker to execute a successful attack.

This stages are ordered chronologically.

### **Reconnaissance**

Upon analysis of the traffic captured in the **netmon.pcap** file, a suspicious IP (192.168.1.122) was detected.

This IP is recorded to navigate between the main and the upload pages several times.

At one point, indicated by the package number **445** and **455** of the capture, this IP tries to login with the usernames, **admin** and **guest** and what appears to be a random password, witch results in unauthorized messages.

### **Credential Access**

- **Brute Force**

  After the previous unsuccessful attempts, a **brute force**
  attack, against the **admin** username, is initiated by the same IP address (package number **621**).

  This attack lasted until package number **6613**, accounting for a total o **2996** password attempts.

  Each one of this attempts resulted in **failure**.

  #### **Prevention**

  Prevention agains brute force attacks relay heavily on restraining the speed, limit and form of attempts of authentication.

  - **Speed**

    One simple way of limiting the speed of the attempts is to create the illusion of loading time of login, this can severely decrease the number of _attempts per minute_, witch will discourage the attacker.

  - **Limit**

    Perhaps the easiest way to prevent this type of attack is to set a limit of attempts per IP address or username. If the limit is met, no more attempts will be allowed, and the user will be notified with a url to reactivate the account's login or change the password.

  - **Form**

    By using **CAPTCHA** or some sort of **two factor authentication (2FA)**, any login attempt will only be complete with a human interaction (in the case of CAPTCHA) and thus preventing programmable and automatic attempts, or with a completely separate authentication device of software (2FA), thus preventing the possibility of successful match with the brute force dictionary resulting in full access to a user's account by the attacker.

- **Credential Forgery**

  Since the privious method was proven unsuccessful, the attacker gives un in trying o login into the service, and will try to **hijack the session** of any already logged in user.

  For this, the attacker begins (in package number **6658**) a series of **_client-side cookie poisoning_** attacks, in an attempt of a match with any user's cookies an thus hijacking said user's session.

  This attack lasted until package **7758**, totalling **50** attempts of _cookie poisoning_.

  This technic also resulted in **failure**.

  #### **Prevention**

  Although none of the attackers attempts to match any of the existing cookies, this could very well have happened. A major security flaw of this service, is the use of **persistent cookies**. This means, that even if a user leaves the website, the cookie remains _alive_, and if captured, could be used to gain access to that user's account.

  This vulnerability can be further explain in the [**CWE-539: Use of Persistent Cookies Containing Sensitive Information**](https://cwe.mitre.org/data/definitions/539.html)

  The prevention for this type of vulnerability passes by implementing **secure session cookies**, ensuring the cookies are unusable once the session is closed. By having comprehensive session management, per example, the service is lacking a way of logging out, one can increase the protection against various attacks, The emplementation of temporary cookies set to expire in a certain time span would also increase changes to resist attacks like _cookie stealing_ and _cookie poisoning_.

### **Resource Development**

### **Execution**

### **Credential Access**

### **Discovery**

### **Collection**

### **Exfiltration**

### **Impact**

## Vulnerabilities

### CWEs Founded

1. [**CWE-539: Use of Persistent Cookies Containing Sensitive Information**](https://cwe.mitre.org/data/definitions/539.html)

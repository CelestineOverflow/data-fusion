#include <ESP8266WiFi.h>
#include <Arduino.h>
#include <String.h>
#include <WiFiUdp.h>
#include <ESP8266mDNS.h>

static String ssid = "Martin Router King";
static String password = "aezakmiQ1";
static WiFiUDP udp;
static IPAddress udp_server;
static int udp_port = 5000;
int init_wifi()
{
    long unsigned int timeout = millis() + 10000;
    Serial.println("Connecting to WiFi");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
        Serial.print(".");
        if (millis() > timeout)
        {
            Serial.println("Timeout");
            // wait_for_new_credentials();
        }
    }
    Serial.println("");
    Serial.print("WiFi connected!");
    Serial.print("IP address: ");
    Serial.println(WiFi.localIP());
    return 0;
}

void scanSerives(){
    if (MDNS.begin("esp8266")) {
        Serial.println("mDNS responder started");
    } else {
        Serial.println("Error setting up MDNS responder!");
    }

    // "http", "tcp": HTTP web servers
    // "https", "tcp": HTTPS web servers
    // "ftp", "tcp": FTP servers
    // "sftp", "tcp": Secure FTP servers
    // "ssh", "tcp": SSH servers
    // "telnet", "tcp": Telnet servers
    // "smb", "tcp": SMB file sharing servers
    // "afpovertcp", "tcp": AFP (Apple Filing Protocol) servers
    // "nfs", "tcp" or "nfs", "udp": NFS file sharing servers
    // "ipp", "tcp": Internet Printing Protocol servers
    // "printer", "tcp": Legacy printer servers
    // "airplay", "tcp": AirPlay servers
    // "raop", "tcp": AirPlay audio streaming (RAOP)
    // "dacp", "tcp": Remote control of AirPlay devices (DACP)
    // "airport", "tcp": Apple AirPort Base Station
    // "homekit", "tcp": Apple HomeKit device
    // "xserveraid", "tcp": Xsan Filesystem Access
    // "webdav", "tcp": WebDAV servers
    String services [] = {"http", "https", "ftp", "sftp", "ssh", "telnet", "smb", "datafusion", "nfs", "ipp", "printer", "airplay", "raop", "dacp", "airport", "homekit", "xserveraid", "webdav"};
    String protocols [] = {"tcp", "udp"};
    for (int i = 0; i < 18; i++)
    {
        for (int j = 0; j < 2; j++)
        {
            Serial.print("Scanning for ");
            Serial.print(services[i]);
            Serial.print(" on ");
            Serial.println(protocols[j]);
            int n = MDNS.queryService(services[i], protocols[j]);
            if (n == 0) {
                Serial.println("no services found");
            } else {
                Serial.print(n);
                Serial.println(" service(s) found");
                for (int i = 0; i < n; ++i) {
                    // Print details for each service found
                    Serial.print("  ");
                    Serial.print(i + 1);
                    Serial.print(": ");
                    Serial.print(MDNS.hostname(i));
                    Serial.print(" (");
                    Serial.print(MDNS.IP(i));
                    Serial.print(":");
                    Serial.print(MDNS.port(i));
                    Serial.println(")");
                }
            }
            Serial.println();
        }
    }
}

int find_service(String service, String protocol)
{
    Serial.print("Scanning for ");
    Serial.print(service);
    Serial.print(" on ");
    Serial.println(protocol);
    //check if MDNS is running
    if (MDNS.begin("esp8266")) {
        Serial.println("mDNS responder started");
    } else {
        Serial.println("Error setting up MDNS responder!");
        return -1;
    }

    int n = MDNS.queryService(service, protocol);
    if (n == 0) {
        Serial.println("no services found");
    } else {
        Serial.print(n);
        Serial.println(" service(s) found");
        for (int i = 0; i < n; ++i) {
            // Print details for each service found
            Serial.print("  ");
            Serial.print(i + 1);
            Serial.print(": ");
            Serial.print(MDNS.hostname(i));
            Serial.print(" (");
            Serial.print(MDNS.IP(i));
            Serial.print(":");
            Serial.print(MDNS.port(i));
            Serial.println(")");
            //Assign the IP address to the udp_server variable
            udp_server = MDNS.IP(i);
            udp_port = MDNS.port(i);
            Serial.print("udp server has been assigned to ");
            Serial.print(udp_server);
            Serial.print(":");
            Serial.println(udp_port);
            return 0;
        }
    }
    return -1;
}

int find_udp_server()
{
    while (1)
    {
        if (find_service("datafusion", "udp") == 0)
        {
            return 0;
        }
        else
        {
            Serial.println("No udp server found");
            delay(1000);
        }
    }
}



int send_data(String data)
{
    udp.beginPacket(udp_server, udp_port);
    udp.write(data.c_str());
    udp.endPacket();
    return 0;
}


# Commands Used

## SELKS / Suricata
- ssh -p 2223 selks@10.92.0.11
- curl -A "Analyst3" http://httpbin.org

## Wireshark
- wireshark /opt/pcaps/sample-200.pcap

## Zeek
- cd ~/logs
- ls
- less conn.log
- less dns.log
- less http.log
- less ssl.log
- less files.log
- less weird.log
- less x509.log
- cat conn.log | zeek-cut -c id.orig_h id.orig_p id.resp_h id.resp_p proto service duration

## RITA
- sudo rita import --rolling ~/logs sample
- rita html-report sample ~/rita-report
- xdg-open ~/logs/sample/index.html

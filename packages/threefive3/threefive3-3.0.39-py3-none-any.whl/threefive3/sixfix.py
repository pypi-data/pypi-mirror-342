"""
sixfix.py
"""

import io
import sys
from functools import partial
from .crc import crc32
from .bitn import NBin
from .stuff import print2
from .stream import Stream, ProgramInfo
from .pmt import PMT

fixme = []


def passed(cue):
    """
    passed a no-op function
    """
    global fixme
    fixme.append(cue.packet_data.pid)
    return cue


class PreFix(Stream):
    """
    PreFix is used to gather 06 Bin data pids with SCTE-35.
    """

    def decode(self, func=passed):
        super().decode(func=passed)
        global fixme
        fixme = list(set(fixme))
        if fixme:
            print("fixing these pids", fixme)
        return fixme


class SixFix(Stream):
    """
    SixFix class
    fixes bin data streams with SCTE-35 to 0x86 SCTE-35 streams
    """

    CUEI_DESCRIPTOR = b"\x05\x04CUEI"

    def __init__(self, tsdata=None):
        super().__init__(tsdata)
        self.pmt_payloads = {}
        self.pmt_headers = set()
        self.pmt_inputs = []
        self.pid_prog = {}
        self.con_pids = set()
        self.out_file = "sixfixed-" + tsdata.rsplit("/")[-1]
        self.in_file = sys.stdin.buffer

    def iter_pkts(self, num_pkts=1):
        """
        iter_pkts iterates a mpegts stream into packets
        """
        return iter(partial(self._tsdata.read, self.PACKET_SIZE * num_pkts), b"")

    def _parse_by_pid(self, pkt, pid):
        ##        if b'\x00\x00\x01' in pkt:
        ##            if b'\x00\x00\x01\xc0' not in pkt:
        ##                print("pid", pid, '  : ', pkt)

        if pid in self.pids.pmt:
            self.pmt_headers.add(pkt[:4])
            self._parse_pmt(pkt[4:], pid)
            prgm = self.pid2prgm(pid)
            if prgm in self.pmt_payloads:
                return self.pmt_payloads[prgm]
        else:
            if pid in self.pids.tables:
                self._parse_tables(pkt, pid)
            return pkt

    def _parse_pkts(self, out_file):
        active = io.BytesIO()
        pkt_count = 0
        chunk_size = 2048
        for pkt in self.iter_pkts():
            pid = self._parse_pid(pkt[1], pkt[2])
            pkt = self._parse_by_pid(pkt, pid)
            if pkt:
                active.write(pkt)
                pkt_count = (pkt_count + 1) % chunk_size
                if not pkt_count:
                    out_file.write(active.getbuffer())
                    active = io.BytesIO()

    def convert_pids(self):
        """
        convert_pids
        changes the stream type to 0x86 and replaces
        the existing PMT as it writes packets to the outfile
        """
        # if isinstance(self.out_file, str):
        #    self.out_file = open(self.out_file, "wb")
        with open(self.out_file, "wb") as out_file:
            self._parse_pkts(out_file)

    def _chk_payload(self, pay, pid):
        pay = self._chk_partial(pay, pid, self._PMT_TID)
        ##        if not pay:
        ##            return False
        return pay

    def _unpad_pmt(self, pay):
        while pay[-1] == 255:
            pay = pay[:-1]
        return pay

    def pmt2packets(self, pmt, program_number):
        """
        pmt2packets split the new pmt table into 188 byte packets
        """
        pmt = list(self.pmt_headers)[0] + b"\x00" + pmt.mk()
        if len(pmt) < 188:
            pad = (188 - len(pmt)) * b"\xff"
            self.pmt_payloads[program_number] = pmt + pad
        else:
            one = pmt[:188]
            two = b""
            pointer = len(pmt[188:])
            three = b""
            pad2 = b""
            pad3 = b""
            #   pointer =pointer.to_bytes(1,byteorder="big")
            if len(self.pmt_headers) > 1:
                two = list(self.pmt_headers)[1] + pmt[188:]
                if len(self.pmt_headers) > 2:
                    three = list(self.pmt_headers)[2] + two[188:]
                    two = two[:188]
                    if len(three) < 188:
                        pad3 = (188 - len(three)) * b"\xff"
                elif len(two) < 188:
                    pad2 = (188 - len(two)) * b"\xff"

            self.pmt_payloads[program_number] = one + two + pad2 + three + pad3
        return True

    def _pmt_precheck(self, pay, pid):
        pay = self._unpad_pmt(pay)
        pay = self._chk_payload(pay, pid)
        if not pay:
            return False
        if pay in self.pmt_inputs:
            return False
        self.pmt_inputs.append(pay)
        return pay

    def _parse_pmt(self, pay, pid):
        """
        parse program maps for streams
        """
        pay = self._pmt_precheck(pay, pid)
        if not pay:
            return False
        pmt = PMT(pay, self.con_pids)
        seclen = self._parse_length(pay[1], pay[2])
        n_seclen = seclen + 6
        if self._section_incomplete(pay, pid, seclen):
            return False
        program_number = self._parse_program(pay[3], pay[4])
        if not program_number:
            return False
        pcr_pid = self._parse_pid(pay[8], pay[9])
        if program_number not in self.maps.prgm:
            self.maps.prgm[program_number] = ProgramInfo()
        pinfo = self.maps.prgm[program_number]
        pinfo.pid = pid
        pinfo.pcr_pid = pcr_pid
        self.pids.pcr.add(pcr_pid)
        self.maps.pid_prgm[pcr_pid] = program_number
        self.maps.pid_prgm[pid] = program_number
        proginfolen = self._parse_length(pay[10], pay[11])
        idx = 12
        n_proginfolen = proginfolen + len(self.CUEI_DESCRIPTOR)
        end = idx + proginfolen
        info_bites = pay[idx:end]
        n_info_bites = self.CUEI_DESCRIPTOR + info_bites
        idx = 12 + proginfolen
        si_len = seclen - (9 + proginfolen)  #  ???
        n_streams = self._parse_program_streams(si_len, pay, idx, program_number)
        # self._regen_pmt(program_number,n_seclen, pcr_pid, n_proginfolen, n_info_bites, n_streams)
        return self.pmt2packets(pmt, program_number)

    def _parse_program_streams(self, si_len, pay, idx, program_number):
        """
        parse the elementary streams
        from a program
        """
        chunk_size = 5
        end_idx = (idx + si_len) - 4
        start = idx
        while idx < end_idx:
            pay, stream_type, pid, ei_len = self._parse_stream_type(pay, idx)
            idx += chunk_size
            idx += ei_len
            self.maps.pid_prgm[pid] = program_number
            self._set_scte35_pids(pid, stream_type)
        streams = pay[start:end_idx]
        return streams

    def _parse_stream_type(self, pay, idx):
        """
        extract stream pid and type
        """
        npay = pay
        stream_type = pay[idx]
        el_pid = self._parse_pid(pay[idx + 1], pay[idx + 2])
        #       if el_pid in self.con_pids:
        if stream_type == 0x6:
            stream_type = 0x86
            npay = pay[:idx] + b"\x86" + pay[idx + 1 :]
        ei_len = self._parse_length(pay[idx + 3], pay[idx + 4])
        self._set_scte35_pids(el_pid, stream_type)
        return npay, stream_type, el_pid, ei_len


def sixfix(arg):
    """
    sixfix converts 0x6 bin data mpegts streams
    that contain SCTE-35 data to stream type 0x86
    """
    global fixme
    fixme = []
    s1 = PreFix(arg)
    sixed = s1.decode(func=passed)

    if not sixed:
        print2("No bin data streams containing SCTE-35 data were found.")
        return
    s2 = SixFix(arg)
    s2.con_pids = sixed
    s2.convert_pids()
    print2(f'Wrote: sixfixed-{arg.rsplit("/")[-1]}\n')
    return


if __name__ == "__main__":
    sixfix(sys.argv[1])

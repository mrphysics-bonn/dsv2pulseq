"""
Read a dsv INF file and append blocks to sequence
"""

def find_char(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

                
# WIP: set RF and Grad shapes -> use running index for shapes
# WIP: INF file is different for VB/VD
def read_dsv_inf(file, seq):
    """ Read INF dsv file (VE)
    """

    with open(file, 'r') as f:
        line_ix = float('inf')
        block_idx = -1
        for k,line in enumerate(f):
            if 'EventBlock' in line:
                block_idx = seq.n_blocks
                duration = int(line[line.rfind(' '):])
                seq.add_block(block_idx, duration)
            if 'Rel.Time' in line:
                ix = find_char(line, '|') # position of events in line
                line_ix = k+2
                ts_old = 0
                freq_phase = None
            if '|' not in line:
                # end of event block
                line_ix = float('inf')
                ts = -1
            if k>=line_ix:
                block = seq.get_block(block_idx)
                ts = int(line[ix[0]+1:ix[1]].strip())
                block.add_timestamp(ts)

                if ts != ts_old and freq_phase is not None:
                    block.set_freqphase(freq_phase, ts_old)
                    freq_phase = None

                if line[ix[1]+1:ix[2]].strip():
                    rf_str = line[ix[1]+1:ix[2]].strip()
                    rf_dur = int(rf_str[rf_str.rfind('/')+1:].strip())
                    rf_shp = [] # WIP: find correct index for seq.rf_val
                    block.add_rf(rf_dur, rf_shp, ts)
                if line[ix[2]+1:ix[3]].strip():
                    freqphase_str = line[ix[2]+1:ix[3]].strip()
                    freq = float(freqphase_str[freqphase_str.rfind(':')+1:freqphase_str.rfind('/')].strip())
                    phase = float(freqphase_str[freqphase_str.rfind('/')+1:].strip())
                    freq_phase = [freq, phase]
                if line[ix[4]+1:ix[5]].strip():
                    adc_str = line[ix[4]+1:ix[5]].strip()
                    adc_samples = float(adc_str[adc_str.rfind(':')+1:adc_str.rfind('/')].strip())
                    adc_dur = float(adc_str[adc_str.rfind('/')+1:].strip())
                    block.add_adc(adc_dur, adc_samples, ts)
                if line[ix[5]+1:ix[6]].strip():
                    gx_str = line[ix[5]+1:ix[6]].strip()
                    gx_ix = find_char(gx_str, '/')
                    gx_amp = float(gx_str[gx_str.rfind(':')+1:gx_ix[0]].strip())
                    gx_rut = int(gx_str[gx_ix[0]+1:gx_ix[1]].strip())
                    gx_dur = int(gx_str[gx_ix[1]+1:gx_ix[2]].strip())
                    gx_rdt = int(gx_str[gx_ix[2]+1:].strip())
                    gx_shp = []
                    block.add_grad('x', gx_amp, gx_dur, gx_rut, gx_rdt, gx_shp, ts)
                if line[ix[6]+1:ix[7]].strip():
                    gy_str = line[ix[6]+1:ix[7]].strip()
                    gy_ix = find_char(gy_str, '/')
                    gy_amp = float(gy_str[gy_str.rfind(':')+1:gy_ix[0]].strip())
                    gy_rut = int(gy_str[gy_ix[0]+1:gy_ix[1]].strip())
                    gy_dur = int(gy_str[gy_ix[1]+1:gy_ix[2]].strip())
                    gy_rdt = int(gy_str[gy_ix[2]+1:].strip())
                    gy_shp = []
                    block.add_grad('y', gy_amp, gy_dur, gy_rut, gy_rdt, gy_shp, ts)
                if line[ix[7]+1:ix[8]].strip():
                    gz_str = line[ix[7]+1:ix[8]].strip()
                    gz_ix = find_char(gz_str, '/')
                    gz_amp = float(gz_str[gz_str.rfind(':')+1:gz_ix[0]].strip())
                    gz_rut = int(gz_str[gz_ix[0]+1:gz_ix[1]].strip())
                    gz_dur = int(gz_str[gz_ix[1]+1:gz_ix[2]].strip())
                    gz_rdt = int(gz_str[gz_ix[2]+1:].strip())
                    gz_shp = []
                    block.add_grad('z', gz_amp, gz_dur, gz_rut, gz_rdt, gz_shp, ts)
                if line[ix[8]+1:ix[9]].strip():
                    trig_str = line[ix[8]+1:ix[9]].strip()
                    trig_type = trig_str[trig_str.rfind(':')+1:trig_str.rfind('/')].strip()
                    trig_dur = int(trig_str[trig_str.rfind('/')+1:].strip())
                    block.add_trig(trig_dur, trig_type, ts)

                ts_old = ts
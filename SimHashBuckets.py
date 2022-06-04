import hashlib


def generate_instances():
    for instance in input().strip().split(' '):
        yield instance


def generate_simhashes():
    N = int(input())
    if N > 100000:
        raise Exception('N must be less than 1000!')
    sh = []
    for _ in range(N):
        sh.append(simhash())
    return N, sh


def generate_queries():
    Q = int(input())
    if Q > 100000:
        raise Exception('Q must be less than 1000!')
    qs = []
    for _ in range(Q):
        qs.append(tuple([int(i) for i in input().strip().split(' ')]))
    return Q, qs


def simhash():
    length = 128
    sh = [0] * length
    for instance in generate_instances():
        md5_hash = hashlib.md5(instance.encode('utf-8')).hexdigest()
        binary_md5_hash = format(int(md5_hash, 16), f'0>{length}b')
        for i in range(length):
            if binary_md5_hash[i] == '1':
                sh[i] += 1
            else:
                sh[i] -= 1
    for i in range(length):
        if sh[i] >= 0:
            sh[i] = 1
        else:
            sh[i] = 0
    return ''.join([str(i) for i in sh])


def hamming_distance(simhash1, simhash2):
    return sum(sh1 != sh2 for sh1, sh2 in zip(simhash1, simhash2))


def hash_to_int(simhash_i, band):
    return int(simhash_i[128 - (band * 16 + 16):128 - band * 16], 2)


if __name__ == '__main__':
    N, simhashes = generate_simhashes()
    Q, queries = generate_queries()

    candidates = {}
    bands = 8
    for band in range(bands):
        buckets = {}
        for i in range(N):
            simhash_i = simhashes[i]
            bucket_id = hash_to_int(simhash_i, band)
            hashes_in_bucket = set()
            if bucket_id in buckets and buckets.get(bucket_id):
                hashes_in_bucket = buckets[bucket_id]
                for h in hashes_in_bucket:
                    if i not in candidates:
                        candidates[i] = set()
                    if h not in candidates:
                        candidates[h] = set()
                    candidates[i].add(h)
                    candidates[h].add(i)
            else:
                hashes_in_bucket = set()
            hashes_in_bucket.add(i)
            buckets[bucket_id] = hashes_in_bucket

    for I, K in queries:
        if I < 0 or I > N - 1 or K < 0 or K > 31:
            continue
        counter = 0
        simhash_i = simhashes[I]
        if I in candidates:
            for candidate in candidates[I]:
                if hamming_distance(simhashes[candidate], simhash_i) <= K:
                    counter += 1
            print(counter)

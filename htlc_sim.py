from hashlib import sha256
import time

# --- HTLC Parameters ---
secret = b"mySecret123"
timeout_seconds = 21 * 60  # 21 minutes

# Public keys (placeholders)
alice_pubkey = "03abcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdefabcdef"
bob_pubkey   = "02fedcbafedcbafedcbafedcbafedcbafedcbafedcbafedcbafedcbafedcba"

# --- Compute HASH160(secret) ---
def hash160(b):
    from hashlib import new
    ripemd160 = new('ripemd160')
    ripemd160.update(sha256(b).digest())
    return ripemd160.digest()

hash_secret = hash160(secret)

# --- Simulate HTLC ---
start_time = time.time()

def claim_alice(provided_secret):
    if hash160(provided_secret) == hash_secret:
        print("✅ Alice claimed funds successfully!")
    else:
        print("❌ Alice's secret is incorrect. Cannot claim.")

def refund_bob():
    elapsed = time.time() - start_time
    if elapsed >= timeout_seconds:
        print("✅ Bob refunded successfully after timeout!")
    else:
        remaining = int(timeout_seconds - elapsed)
        print(f"❌ Timeout not reached. Bob must wait {remaining} seconds.")

# --- Testing ---

print("=== Simulate Alice Claiming ===")
claim_alice(secret)             # Correct secret
claim_alice(b"wrongSecret")     # Wrong secret

print("\n=== Simulate Bob Refund ===")
refund_bob()                     # Before 21 minutes

# Optional: simulate time passing
print("\n=== Simulate Bob Refund after timeout ===")
time.sleep(1)  # In real test, you would wait timeout_seconds or mock time
start_time -= timeout_seconds   # Trick to simulate timeout reached
refund_bob()

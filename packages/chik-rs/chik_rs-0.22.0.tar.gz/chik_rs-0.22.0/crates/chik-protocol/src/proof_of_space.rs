use crate::bytes::{Bytes, Bytes32};
use chik_bls::G1Element;
use chik_streamable_macro::streamable;

#[streamable]
pub struct ProofOfSpace {
    challenge: Bytes32,
    pool_public_key: Option<G1Element>,
    pool_contract_puzzle_hash: Option<Bytes32>,
    plot_public_key: G1Element,
    size: u8,
    proof: Bytes,
}

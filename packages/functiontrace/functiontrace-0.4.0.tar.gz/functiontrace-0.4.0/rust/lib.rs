#[pyo3::pymodule]
mod _lib {
    use pyo3::prelude::*;
    use std::ffi::{CStr, OsStr};
    use std::os::raw::c_char;
    use std::os::unix::ffi::OsStrExt;
    use std::os::unix::net::UnixStream;

    ////////////////////////////////////////////////////////////////////////////////////////////////
    // Socket Communication
    ////////////////////////////////////////////////////////////////////////////////////////////////

    /// Initializes and returns a pointer to the [`UnixStream`] we'll communicate to
    /// `functiontrace-server` on.
    ///
    /// The returned value will be stored as [`MpackWriter.context`] and used by [`Mpack_Flush`].
    #[pyfunction]
    fn message_initialization(socket: usize) -> usize {
        let c_socket = unsafe {
            // SAFETY: socket is a valid `char*` converted via `PyLong_FromVoidPtr`.
            CStr::from_ptr(socket as *const c_char)
        };
        let sockaddr = OsStr::from_bytes(c_socket.to_bytes());

        // The functiontrace-server might not be ready to receive connections yet, so we retry for
        // a bit.
        let start = std::time::Instant::now();
        let socket = loop {
            match UnixStream::connect(sockaddr) {
                Ok(s) => {
                    break Box::new(s);
                }
                _ => {
                    if start.elapsed() > std::time::Duration::from_millis(1000) {
                        panic!("Timed out trying to connect to functiontrace-server");
                    }

                    std::thread::sleep(std::time::Duration::from_millis(10));
                }
            }
        };

        // This must be freed by `message_shutdown`
        Box::into_raw(socket) as usize
    }

    /// Shutdown a socket that was opened by [`message_initialize`], triggering
    /// `functiontrace-server` to read the data sent over it.
    ///
    /// If we forget this, we'll leak sockets and a bit of memory.
    #[pyfunction]
    fn message_shutdown(socket: usize) {
        let socket = unsafe {
            // SAFETY: socket is a `UnixStream` emitted from `message_initialization` encoded via
            // `PyLong_FromVoidPtr`.
            Box::from_raw(socket as *mut UnixStream)
        };

        if let Err(e) = socket.shutdown(std::net::Shutdown::Both) {
            panic!("Failed to close socket: {e}");
        }
    }

    /// The initial subset of the `mpack_writer_t` struct, which `mpack.h` will use to pass us our
    /// per-thread context in.
    #[repr(C)]
    struct MpackWriter {
        flush: *const (),
        error_fn: *const (),
        teardown: *const (),
        context: *mut UnixStream,
    }

    /// Flush events to this socket once the given buffer is full according to `mpack`.
    #[unsafe(no_mangle)]
    extern "C" fn Mpack_Flush(writer: *const MpackWriter, buffer: *const u8, bytes: usize) {
        use std::io::Write;

        let data = unsafe {
            // SAFETY: `bytes` represents the initialized number of bytes in `buffer` when called
            // by `mpack_writer_flush_message`.
            std::slice::from_raw_parts(buffer, bytes)
        };

        let mut socket = unsafe {
            // SAFETY: `writer` is valid and `writer->context` contains a `UnixStream` emitted from
            // `message_initialization`.
            &*(*writer).context
        };
        if let Err(e) = socket.write_all(data) {
            panic!("Socket send failed: {e}");
        }
    }

    /// C accessor for [`Mpack_Flush`]
    #[pyfunction]
    fn message_flush() -> PyResult<usize> {
        Ok(Mpack_Flush as usize)
    }
}

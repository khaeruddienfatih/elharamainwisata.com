<?php
/*
 * Snippet WPCode (PHP Snippet, Auto Insert, Run Everywhere) — SEMENTARA.
 * Membantu login REST API dengan Application Passwords di elharamainwisata.com
 * (ada plugin yang menentukan user terlalu awal) + endpoint diagnosa /wp-json/eh-diag/v1/auth.
 * Saat menempel di WPCode, jangan sertakan baris "<?php" di atas. Hapus snippet setelah selesai.
 */
$GLOBALS['eh_diag'] = array(
	'user_determined_before_snippet' => did_action( 'set_current_user' ) > 0,
);

// Header cadangan bila header Authorization dibuang di tengah jalan (mis. Cloudflare).
if ( empty( $_SERVER['PHP_AUTH_USER'] ) && empty( $_SERVER['HTTP_AUTHORIZATION'] ) && ! empty( $_SERVER['HTTP_X_EH_AUTH'] ) ) {
	$eh_decoded = base64_decode( $_SERVER['HTTP_X_EH_AUTH'], true );
	if ( $eh_decoded && strpos( $eh_decoded, ':' ) !== false ) {
		list( $_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW'] ) = explode( ':', $eh_decoded, 2 );
	}
}

// Bila status login sudah "terkunci" sebelum REST, validasi ulang Application Password (pengecekan bawaan WordPress).
add_filter( 'rest_authentication_errors', function ( $result ) {
	if ( ! empty( $result ) || is_user_logged_in() ) {
		return $result;
	}
	if ( empty( $_SERVER['PHP_AUTH_USER'] ) || empty( $_SERVER['PHP_AUTH_PW'] ) ) {
		return $result;
	}
	$user = wp_authenticate_application_password( null, $_SERVER['PHP_AUTH_USER'], $_SERVER['PHP_AUTH_PW'] );
	if ( $user instanceof WP_User ) {
		wp_set_current_user( $user->ID );
		return true;
	}
	return $result;
}, 5 );

// Endpoint diagnosa: hanya mengembalikan true/false, tanpa data rahasia.
add_action( 'rest_api_init', function () {
	register_rest_route( 'eh-diag/v1', '/auth', array(
		'methods'             => 'GET',
		'permission_callback' => '__return_true',
		'callback'            => function () {
			return array_merge( $GLOBALS['eh_diag'], array(
				'has_http_authorization'          => ! empty( $_SERVER['HTTP_AUTHORIZATION'] ),
				'has_redirect_http_authorization' => ! empty( $_SERVER['REDIRECT_HTTP_AUTHORIZATION'] ),
				'has_php_auth_user'               => ! empty( $_SERVER['PHP_AUTH_USER'] ),
				'has_x_eh_auth'                   => ! empty( $_SERVER['HTTP_X_EH_AUTH'] ),
				'app_passwords_available'         => wp_is_application_passwords_available(),
				'logged_in'                       => is_user_logged_in(),
			) );
		},
	) );
} );

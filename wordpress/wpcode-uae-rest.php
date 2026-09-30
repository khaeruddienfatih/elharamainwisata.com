<?php
/*
 * Snippet WPCode (PHP Snippet, Auto Insert, Run Everywhere) — endpoint REST untuk header/footer UAE.
 * Dipasang di haji.biz, elharamainhaji.com, elharamain.id supaya Claude bisa membuat/memperbarui
 * template UAE (post type elementor-hf) otomatis. TIDAK mengubah proses login (beda dari snippet bantu-login).
 * Hanya admin (manage_options) yang login via Application Password yang bisa memakai endpoint ini.
 * Saat menempel di WPCode, jangan sertakan baris "<?php" di atas.
 *
 * GET  /wp-json/eh/v1/hf              daftar template UAE + pengaturan tampilnya
 * POST /wp-json/eh/v1/hf              {id?, title, type: header|footer, html, status?: publish|draft}
 *      membuat (tanpa id) atau memperbarui (dengan id) template berisi 1 widget HTML, tampil di seluruh situs.
 */
add_action( 'rest_api_init', function () {
	$can = function () {
		return current_user_can( 'manage_options' );
	};

	register_rest_route( 'eh/v1', '/hf', array(
		array(
			'methods'             => 'GET',
			'permission_callback' => $can,
			'callback'            => function () {
				$out = array();
				foreach ( get_posts( array( 'post_type' => 'elementor-hf', 'post_status' => 'any', 'numberposts' => 50 ) ) as $p ) {
					$meta = array();
					foreach ( get_post_meta( $p->ID ) as $k => $v ) {
						if ( 0 === strpos( $k, 'ehf_' ) || in_array( $k, array( '_elementor_edit_mode', '_elementor_template_type' ), true ) ) {
							$meta[ $k ] = maybe_unserialize( $v[0] );
						}
					}
					$out[] = array(
						'id'     => $p->ID,
						'title'  => $p->post_title,
						'status' => $p->post_status,
						'meta'   => $meta,
						'data'   => json_decode( (string) get_post_meta( $p->ID, '_elementor_data', true ), true ),
					);
				}
				return $out;
			},
		),
		array(
			'methods'             => 'POST',
			'permission_callback' => $can,
			'callback'            => function ( WP_REST_Request $r ) {
				$type = $r->get_param( 'type' );
				$html = (string) $r->get_param( 'html' );
				if ( ! in_array( $type, array( 'header', 'footer' ), true ) || '' === $html ) {
					return new WP_Error( 'eh_bad_request', 'type (header|footer) dan html wajib diisi', array( 'status' => 400 ) );
				}
				$id     = (int) $r->get_param( 'id' );
				$status = in_array( $r->get_param( 'status' ), array( 'publish', 'draft' ), true ) ? $r->get_param( 'status' ) : 'publish';
				if ( $id && 'elementor-hf' !== get_post_type( $id ) ) {
					return new WP_Error( 'eh_not_hf', 'ID bukan template UAE', array( 'status' => 400 ) );
				}
				$post = array(
					'post_type'   => 'elementor-hf',
					'post_title'  => $r->get_param( 'title' ) ?: ucfirst( $type ),
					'post_status' => $status,
				);
				if ( $id ) {
					$post['ID'] = $id;
					$id         = wp_update_post( $post, true );
				} else {
					$id = wp_insert_post( $post, true );
				}
				if ( is_wp_error( $id ) ) {
					return $id;
				}
				$zero = array( 'unit' => 'px', 'top' => '0', 'right' => '0', 'bottom' => '0', 'left' => '0', 'isLinked' => true );
				$data = array( array(
					'id' => 'eh' . $id . 's', 'elType' => 'section', 'isInner' => false,
					'settings' => array( 'layout' => 'full_width', 'gap' => 'no', 'padding' => $zero ),
					'elements' => array( array(
						'id' => 'eh' . $id . 'c', 'elType' => 'column', 'isInner' => false,
						'settings' => array( '_column_size' => 100, 'padding' => $zero ),
						'elements' => array( array(
							'id' => 'eh' . $id . 'w', 'elType' => 'widget', 'widgetType' => 'html', 'isInner' => false,
							'settings' => array( 'html' => $html ), 'elements' => array(),
						) ),
					) ),
				) );
				update_post_meta( $id, '_elementor_data', wp_slash( wp_json_encode( $data ) ) );
				update_post_meta( $id, '_elementor_edit_mode', 'builder' );
				update_post_meta( $id, '_elementor_template_type', 'wp-post' );
				if ( defined( 'ELEMENTOR_VERSION' ) ) {
					update_post_meta( $id, '_elementor_version', ELEMENTOR_VERSION );
				}
				// Pengaturan tampil UAE: seluruh situs, semua pengguna.
				update_post_meta( $id, 'ehf_template_type', 'type_' . $type );
				update_post_meta( $id, 'ehf_target_include_locations', array( 'rule' => array( 'basic-global' ), 'specific' => array() ) );
				update_post_meta( $id, 'ehf_target_exclude_locations', array( 'rule' => array(), 'specific' => array() ) );
				update_post_meta( $id, 'ehf_target_user_roles', array( 'all' ) );
				if ( class_exists( '\Elementor\Plugin' ) ) {
					\Elementor\Plugin::$instance->files_manager->clear_cache();
				}
				do_action( 'litespeed_purge_all' );
				return array( 'id' => $id, 'status' => get_post_status( $id ), 'edit' => admin_url( 'post.php?post=' . $id . '&action=elementor' ) );
			},
		),
	) );
} );

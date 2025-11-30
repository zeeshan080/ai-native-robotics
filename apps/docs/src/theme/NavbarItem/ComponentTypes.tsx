import ComponentTypes from '@theme-original/NavbarItem/ComponentTypes';
import NavbarAuthButton from '@site/src/components/NavbarAuthButton';

/**
 * Register custom navbar component types
 *
 * This allows us to use custom components in docusaurus.config.ts navbar.items
 * by setting type: 'custom-navbarAuthButton'
 */
export default {
  ...ComponentTypes,
  'custom-navbarAuthButton': NavbarAuthButton,
};
